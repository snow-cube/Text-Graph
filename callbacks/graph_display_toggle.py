from dash import html, Input, Output, State
import dash_cytoscape as cyto
from text_graph import TextGraph
from styles.basic_style import get_base_stylesheet, get_reset_style_state
from callbacks.upload import NODE_THRESHOLD


def register_graph_display_toggle_callback(app):
    @app.callback(
        Output("graph-container", "children"),
        Output("graph-display-state", "data"),
        Output("style-store", "data"),  # 添加style-store作为输出
        Output("graph-display-toggle", "value"),  # 添加对切换开关的控制
        Output("graph-display-toggle", "options"),  # 添加对选项的控制
        Input("graph-display-toggle", "value"),
        Input("graph-store", "data"),
        State("graph-display-state", "data"),
        State("style-store", "data"),  # 添加当前style-store状态作为输入
    )
    def toggle_graph_component(toggle_value, graph_data, current_state, current_style):
        show_graph = "show" in toggle_value
        is_locked = current_state.get("locked", False)

        # 检查数据规模
        node_count = 0
        if graph_data:
            text_graph = TextGraph(graph_data)
            node_count = len(text_graph.nodes)

            # 如果节点数超过阈值，强制锁定显示
            if node_count > NODE_THRESHOLD:
                is_locked = True
                show_graph = False

        # 更新状态
        current_state["show"] = show_graph
        current_state["locked"] = is_locked

        # 确定切换开关的状态和选项
        toggle_options = [
            {
                "label": f" 显示图形可视化{'（已锁定）' if is_locked else ''}",
                "value": "show",
                "disabled": is_locked,
            }
        ]
        toggle_value = [] if not show_graph else ["show"]

        # Reset the data_updated flag if it exists
        if "data_updated" in current_state:
            current_state["data_updated"] = False

        # 初始化重置后的样式数据
        # reset_style = {
        #     "selected_nodes": [],
        #     "bridge_words": [],
        #     "highlighted_edges": [],
        #     "base_style_applied": True,
        # }
        reset_style = get_reset_style_state()

        if show_graph:
            # 显示图组件时，重置style-store
            return (
                [
                    cyto.Cytoscape(
                        id="cytoscape",
                        elements=(
                            TextGraph(graph_data).get_elements() if graph_data else []
                        ),
                        layout={"name": "cose", "padding": 50},
                        style={
                            "width": "100%",
                            "height": "700px",
                            "border": "1px solid #ddd",
                            "borderRadius": "5px",
                        },
                        generateImage={"type": "png", "action": "store"},
                        stylesheet=get_base_stylesheet(),
                    ),
                    # 清空选中按钮
                    html.Button(
                        "清空所有选中",
                        id="clear-selection-btn",
                        n_clicks=0,
                        style={
                            "position": "absolute",
                            "top": "18px",
                            "right": "18px",
                            "zIndex": 10,
                            "fontSize": "15px",
                            "padding": "7px 18px",
                            "backgroundColor": "#ffb300",
                            "color": "#fff",
                            "border": "none",
                            "borderRadius": "4px",
                            "cursor": "pointer",
                            "boxShadow": "0 2px 8px #e0e0e0",
                        },
                    ),
                    # 保存图片按钮 - 添加到图右下角
                    html.Button(
                        "保存为图片",
                        id="save-image-btn",
                        n_clicks=0,
                        style={
                            "position": "absolute",
                            "bottom": "18px",
                            "right": "18px",
                            "zIndex": 10,
                            "fontSize": "15px",
                            "padding": "7px 18px",
                            "backgroundColor": "#00A8E8",
                            "color": "#fff",
                            "border": "none",
                            "borderRadius": "4px",
                            "cursor": "pointer",
                            "boxShadow": "0 2px 8px #e0e0e0",
                        },
                    ),
                ],
                current_state,
                reset_style,
                toggle_value,
                toggle_options,
            )
        else:
            # 不显示图组件时，保持当前style-store状态不变
            return (
                [
                    html.Div(
                        "图形可视化已隐藏"
                        + ("（数据量过大，已锁定）" if is_locked else "（节省资源）"),
                        style={
                            "display": "flex",
                            "justifyContent": "center",
                            "alignItems": "center",
                            "height": "700px",
                            "border": "1px dashed #ccc",
                            "borderRadius": "5px",
                            "color": "#666",
                            "fontSize": "16px",
                            "backgroundColor": "#f9f9f9",
                        },
                    )
                ],
                current_state,
                current_style,
                toggle_value,
                toggle_options,
            )
