from dash import Output, Input, State, html, ctx, ALL
from graph_utils import TextGraph
from style_utils import (
    get_base_stylesheet,
    get_selected_node_style,
    get_in_edge_style,
    get_out_edge_style,
)
import dash

def get_bridge_word_style(word):
    # 橙黄色高亮桥接词节点，弱于选中节点
    return {
        "selector": f"node[id = '{word}']",
        "style": {
            "background-color": "#ffe082",  # 柔和橙黄
            "border-color": "#ffb300",
            "border-width": 3,
            "text-outline-color": "#ffb300",
            "shadow-color": "#ffe082",
            "shadow-blur": 8,
            "shadow-opacity": 0.5,
            "font-size": "18px",
            "z-index": 2,
        },
    }

def register_callbacks(app):
    # 创建共享函数处理桥接词逻辑
    def process_bridge_words(word1, word2, text_graph, elements, style_state):
        """处理桥接词的通用函数

        Args:
            word1: 第一个单词
            word2: 第二个单词
            text_graph: TextGraph实例或原始文本
            elements: 图的元素列表
            style_state: 当前样式状态字典

        Returns:
            tuple: (桥接词列表, 信息消息, 更新后的样式状态)
        """
        # 确保有TextGraph实例
        if isinstance(text_graph, str):
            tg = TextGraph(text_graph or "")
        else:
            tg = text_graph

        # 验证输入
        if not word1 or not word2 or word1 == word2:
            return [], f"请提供两个不同的单词", style_state

        # 查询桥接词
        bridges = tg.get_bridge_words(word1, word2)

        # 更新样式状态：选中的两个端点节点
        style_state["selected_nodes"] = [word1, word2]
        style_state["bridge_words"] = bridges

        # 添加桥接词相关的边到高亮列表
        highlighted_edges = []
        if bridges and elements and isinstance(elements, list):
            for elem in elements:
                data = elem.get("data", {})
                if "source" in data and "target" in data:
                    # 从word1到桥接词的边
                    if data.get("source") == word1 and data.get("target") in bridges:
                        highlighted_edges.append({"source": word1, "target": data.get("target"), "type": "bridge"})
                    # 从桥接词到word2的边
                    if data.get("source") in bridges and data.get("target") == word2:
                        highlighted_edges.append({"source": data.get("source"), "target": word2, "type": "bridge"})

        style_state["highlighted_edges"] = highlighted_edges

        # 构建消息
        if bridges:
            msg = f"桥接词（{word1} → ? → {word2}）：" + "，".join(bridges)
        else:
            msg = f"未找到 {word1} → ? → {word2} 的桥接词"

        return bridges, msg, style_state

    @app.callback(
        Output("cytoscape", "elements"),
        Output("file-info", "children"),
        Output("node-info", "children", allow_duplicate=True),
        Output("style-store", "data"),  # 更新为使用样式存储
        Output("graph-store", "data"),
        Input("upload-data", "contents"),
        State("upload-data", "filename"),
        State("style-store", "data"),  # 读取当前样式状态
        prevent_initial_call=True,
    )
    def update_output(content, filename, style_state):
        if content and filename.endswith(".txt"):
            import base64

            _, b64_content = content.split(",")
            decoded = base64.b64decode(b64_content).decode("utf-8")
            tg = TextGraph(decoded)
            elements = tg.get_elements()

            # 重置样式状态
            style_state = {
                "selected_nodes": [],
                "bridge_words": [],
                "highlighted_edges": [],
                "base_style_applied": True
            }

            return (
                elements,
                f"已成功上传并解析文件：{filename}",
                "请点击一个节点查看详细信息",
                style_state,
                decoded,  # 存储原始文本
            )

        # 重置样式状态
        style_state = {
            "selected_nodes": [],
            "bridge_words": [],
            "highlighted_edges": [],
            "base_style_applied": True
        }

        return [], "❌ 文件格式错误，仅支持 .txt", "", style_state, ""

    @app.callback(
        [
            Output("node-info", "children", allow_duplicate=True),
            Output("style-store", "data", allow_duplicate=True),
            Output("bridge-word1", "value", allow_duplicate=True),
            Output("bridge-word2", "value", allow_duplicate=True),
            Output("bridge-result", "children", allow_duplicate=True),
        ],
        [Input("cytoscape", "tapNodeData")],
        [
            State("style-store", "data"),
            State("cytoscape", "elements"),
            State("graph-store", "data"),
            State("bridge-word1", "value"),
            State("bridge-word2", "value"),
        ],
        prevent_initial_call=True,
    )
    def handle_node_click(tap_node_data, style_state, elements, graph_text, curr_word1, curr_word2):
        # 如果没有点击节点，不进行处理
        if not tap_node_data:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

        # 获取点击的节点标签
        clicked_word = tap_node_data["label"]

        # 获取当前选中的节点
        selected_nodes = style_state.get("selected_nodes", [])

        # 如果点击的节点已经在选中列表中，则将其移除（切换选择）
        if clicked_word in selected_nodes:
            selected_nodes.remove(clicked_word)
        else:
            # 如果不在选中列表中，则添加它
            selected_nodes.append(clicked_word)

        # 更新样式状态中的选中节点
        style_state["selected_nodes"] = selected_nodes

        # 处理刚好选中两个节点的情况（桥接词查询）
        if len(selected_nodes) == 2:
            w1, w2 = selected_nodes

            # 使用共享处理函数查询桥接词
            bridges, msg, updated_style = process_bridge_words(w1, w2, graph_text, elements, style_state)
            return dash.no_update, updated_style, w1, w2, msg

        # 清除桥接词和高亮边
        style_state["bridge_words"] = []
        style_state["highlighted_edges"] = []

        # 如果选中了一个节点，显示节点详情
        if len(selected_nodes) == 1:
            word = selected_nodes[0]

            # 记录高亮的边
            highlighted_edges = []

            # 收集入边和出边信息用于显示和样式高亮
            in_edges = []
            out_edges = []
            if isinstance(elements, list):
                for elem in elements:
                    data = elem.get("data", {})
                    if "source" in data and "target" in data:
                        if data["target"] == word:
                            in_edges.append((data["source"], data.get("weight", 1)))
                            highlighted_edges.append({"source": data["source"], "target": word, "type": "in"})
                        elif data["source"] == word:
                            out_edges.append((data["target"], data.get("weight", 1)))
                            highlighted_edges.append({"source": word, "target": data["target"], "type": "out"})

            style_state["highlighted_edges"] = highlighted_edges

            info_components = [
                html.H4(f"单词: {word}", style={"color": "#0077B6"}),
                html.Hr(),
                html.Div(
                    [
                        html.H5("入边 (前驱词):", style={"color": "#444"}),
                        (
                            html.Ul(
                                [
                                    html.Li(f"{source} → {word} (权重: {weight})")
                                    for source, weight in sorted(in_edges, key=lambda x: -x[1])
                                ]
                            )
                            if in_edges
                            else html.P("无入边")
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.H5("出边 (后继词):", style={"color": "#444"}),
                        (
                            html.Ul(
                                [
                                    html.Li(f"{word} → {target} (权重: {weight})")
                                    for target, weight in sorted(out_edges, key=lambda x: -x[1])
                                ]
                            )
                            if out_edges
                            else html.P("无出边")
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.H5("统计:", style={"color": "#444"}),
                        html.P(f"总前驱单词数: {len(in_edges)}"),
                        html.P(f"总后继单词数: {len(out_edges)}"),
                        html.P(f"总关联单词数: {len(in_edges) + len(out_edges)}"),
                    ]
                ),
            ]
            # 返回节点详情，但保持桥接词输入框和结果不变
            return info_components, style_state, dash.no_update, dash.no_update, dash.no_update

        # 没有选中节点（全部取消选择）或选中了太多节点
        if len(selected_nodes) == 0:
            return "请点击一个节点查看详细信息或选择两个节点查询桥接词", style_state, dash.no_update, dash.no_update, dash.no_update
        else:
            return "请只选择一个节点查看详情或选择恰好两个节点查询桥接词", style_state, dash.no_update, dash.no_update, dash.no_update

    @app.callback(
        Output("cytoscape", "generateImage"),
        Input("save-image-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def save_cytoscape_image(n_clicks):
        if n_clicks:
            return {
                "type": "png",  # 可选: "png", "jpg", "jpeg", "svg"
                "action": "download",  # 直接下载
                "filename": "graph.png",
                "width": 1200,  # 可根据需要调整
                "height": 800,
                "scale": 2,  # 提高分辨率
            }
        return dash.no_update

    @app.callback(
        [
            Output("bridge-word1", "value", allow_duplicate=True),
            Output("bridge-word2", "value", allow_duplicate=True),
            Output("bridge-result", "children", allow_duplicate=True),
            Output("style-store", "data", allow_duplicate=True),
        ],
        [Input("bridge-query-btn", "n_clicks")],
        [
            State("bridge-word1", "value"),
            State("bridge-word2", "value"),
            State("graph-store", "data"),
            State("style-store", "data"),
            State("cytoscape", "elements"),
        ],
        prevent_initial_call=True,
    )
    def query_bridge_words_from_input(n_clicks, word1, word2, graph_text, style_state, elements):
        """处理从输入框输入单词查询桥接词的情况"""
        # 仅处理按钮点击的情况
        if not n_clicks:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update

        # 使用共享处理函数
        bridges, msg, updated_style = process_bridge_words(word1, word2, graph_text, elements, style_state)

        return word1, word2, msg, updated_style

    # 新增：清空所有选中按钮的回调
    @app.callback(
        Output("style-store", "data", allow_duplicate=True),
        Output("node-info", "children", allow_duplicate=True),
        Output("bridge-word1", "value", allow_duplicate=True),
        Output("bridge-word2", "value", allow_duplicate=True),
        Output("bridge-result", "children", allow_duplicate=True),
        Input("clear-selection-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def clear_selection(n_clicks):
        if not n_clicks:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        # 重置样式状态
        style_state = {
            "selected_nodes": [],
            "bridge_words": [],
            "highlighted_edges": [],
            "base_style_applied": True
        }
        return (
            style_state,
            "请点击一个节点查看详细信息或选择两个节点查询桥接词",
            "",
            "",
            "",
        )

    # 新增：中央样式管理回调
    @app.callback(
        Output("cytoscape", "stylesheet"),
        Input("style-store", "data"),
        prevent_initial_call=True
    )
    def update_stylesheet(style_state):
        """根据样式状态更新cytoscape的样式表"""
        stylesheet = get_base_stylesheet()

        selected_nodes = style_state.get("selected_nodes", [])
        # 第一个节点：用原第二个节点的样式（蓝绿）
        if len(selected_nodes) >= 1:
            node1 = selected_nodes[0]
            stylesheet.append({
                "selector": f"node[id = '{node1}']",
                "style": {
                    "background-color": "#26a69a",  # 蓝绿
                    "border-color": "#00897b",
                    "border-width": 4,
                    "text-outline-color": "#00897b",
                    "shadow-color": "#26a69a",
                    "shadow-blur": 13,
                    "shadow-opacity": 0.6,
                    "font-size": "19px",
                    "color": "#fff",
                    "z-index": 8,
                },
            })
        # 第二个节点：用原桥接节点的样式（青绿）
        if len(selected_nodes) >= 2:
            node2 = selected_nodes[1]
            stylesheet.append({
                "selector": f"node[id = '{node2}']",
                "style": {
                    "background-color": "#b2dfdb",  # 柔和青绿
                    "border-color": "#4db6ac",
                    "border-width": 3,
                    "text-outline-color": "#4db6ac",
                    "shadow-color": "#b2dfdb",
                    "shadow-blur": 8,
                    "shadow-opacity": 0.5,
                    "font-size": "18px",
                    "z-index": 2,
                },
            })
        # 其余选中节点（如果有）用更和谐但不显眼的样式（浅蓝灰）
        if len(selected_nodes) > 2:
            for node in selected_nodes[2:]:
                stylesheet.append(get_selected_node_style(node))

        # 桥接词节点样式（橙黄色，弱于选中节点，色调区分）
        for bridge in style_state.get("bridge_words", []):
            stylesheet.append(get_bridge_word_style(bridge))

        # 添加高亮边的样式
        for edge in style_state.get("highlighted_edges", []):
            if edge["type"] == "in":
                stylesheet.append(get_in_edge_style(edge["source"], edge["target"]))
            elif edge["type"] == "out":
                stylesheet.append(get_out_edge_style(edge["source"], edge["target"]))
            elif edge["type"] == "bridge":
                stylesheet.append(get_out_edge_style(edge["source"], edge["target"]))

        return stylesheet
