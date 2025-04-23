import sys
import dash
from dash import html, dcc, Input, Output, State
import dash_cytoscape as cyto
from graph_utils import build_graph_elements_from_text
from dash.dcc import Download
import json
from dash.exceptions import PreventUpdate

# ==== 启动时检查是否提供文件路径 ====
initial_text = ""
if len(sys.argv) == 2:
    try:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            initial_text = f.read()
    except Exception as e:
        print(f"⚠️ 无法读取文件: {e}")

app = dash.Dash(__name__)
app.title = "词图可视化"

app.layout = html.Div(
    [
        html.H2(
            "词图可视化工具（有向图）",
            style={"textAlign": "center", "margin": "20px 0"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        cyto.Cytoscape(
                            id="cytoscape",
                            elements=(
                                build_graph_elements_from_text(initial_text)
                                if initial_text
                                else []
                            ),
                            layout={"name": "cose", "padding": 50},
                            style={
                                "width": "100%",
                                "height": "700px",
                                "border": "1px solid #ddd",
                                "borderRadius": "5px",
                            },
                            generateImage={"type": "png", "action": "store"},
                            stylesheet=[
                                {
                                    "selector": "node",
                                    "style": {
                                        "label": "data(label)",
                                        "background-color": "#00A8E8",
                                        "color": "#FFFFFF",
                                        "font-size": "18px",
                                        "font-weight": "bold",
                                        "text-valign": "center",
                                        "text-halign": "center",
                                        "border-width": 2,
                                        "border-color": "#0077B6",
                                        "shape": "ellipse",
                                        "width": "45px",
                                        "height": "45px",
                                        "text-outline-width": 2,
                                        "text-outline-color": "#0077B6",
                                        "shadow-blur": 10,
                                        "shadow-color": "#aaa",
                                        "shadow-offset-x": 2,
                                        "shadow-offset-y": 2,
                                        "shadow-opacity": 0.5,
                                    },
                                },
                                {
                                    "selector": "node.selected",
                                    "style": {
                                        "background-color": "#FF5733",
                                        "border-color": "#C70039",
                                        "border-width": 4,
                                        "text-outline-color": "#C70039",
                                        "shadow-color": "#FF5733",
                                        "shadow-blur": 15,
                                        "shadow-opacity": 0.8,
                                        "font-size": "20px",
                                    },
                                },
                                {
                                    "selector": "edge.connected",
                                    "style": {
                                        "line-color": "#FF5733",
                                        "target-arrow-color": "#FF5733",
                                        "width": "data(weight)",
                                        "opacity": 1,
                                    },
                                },
                                {
                                    "selector": "edge",
                                    "style": {
                                        "label": "data(weight)",
                                        "curve-style": "bezier",
                                        "target-arrow-shape": "triangle",
                                        "target-arrow-color": "#666",
                                        "line-color": "#666",
                                        "width": "mapData(weight, 1, 10, 2, 6)",
                                        "font-size": "12px",
                                        "color": "#555",
                                    },
                                },
                            ],
                        ),
                    ],
                    style={
                        "width": "65%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                    },
                ),
                html.Div(
                    [
                        # 优化后的按钮区域
                        html.Div(
                            [
                                dcc.Upload(
                                    id="upload-data",
                                    children=html.Button(
                                        "上传文本文件",
                                        style={
                                            "fontSize": "16px",
                                            "padding": "8px 20px",
                                            "marginRight": "12px",
                                            "backgroundColor": "#0077B6",
                                            "color": "#fff",
                                            "border": "none",
                                            "borderRadius": "4px",
                                            "cursor": "pointer",
                                        },
                                    ),
                                    accept=".txt",
                                    multiple=False,
                                ),
                                html.Button(
                                    "保存为图片",
                                    id="save-image-btn",
                                    n_clicks=0,
                                    style={
                                        "fontSize": "16px",
                                        "padding": "8px 20px",
                                        "backgroundColor": "#00A8E8",
                                        "color": "#fff",
                                        "border": "none",
                                        "borderRadius": "4px",
                                        "cursor": "pointer",
                                    },
                                ),
                                html.Div(
                                    id="file-info",
                                    style={
                                        "marginTop": "16px",
                                        "fontSize": "15px",
                                        "textAlign": "center",
                                        "padding": "6px 0",
                                        "borderRadius": "4px",
                                        "backgroundColor": "#eafaf1",
                                        "color": "#218838",
                                        "border": "1px solid #b7e4c7",
                                        "minHeight": "28px",
                                        "transition": "all 0.3s",
                                        "boxShadow": "0 1px 2px #e0e0e0",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justifyContent": "center",
                                "alignItems": "center",
                                "gap": "10px",
                                "marginBottom": "28px",
                                "marginTop": "10px",
                                "padding": "8px 0",
                                "backgroundColor": "#f1f8ff",
                                "borderRadius": "6px",
                                "boxShadow": "0 1px 4px #e0e0e0",
                            },
                        ),
                        html.H3(
                            "节点详细信息",
                            style={
                                "textAlign": "center",
                                "marginTop": "0px",
                                "marginBottom": "10px",
                                "color": "#0077B6",
                                "fontWeight": "bold",
                                "letterSpacing": "2px",
                            },
                        ),
                        html.Div(
                            id="node-info",
                            style={
                                "border": "1px solid #ddd",
                                "padding": "18px 15px",
                                "borderRadius": "7px",
                                "backgroundColor": "#f9f9f9",
                                "minHeight": "540px",
                                "margin": "0px 0",
                                "overflowY": "auto",
                                "boxShadow": "0 1px 6px #e0e0e0",
                            },
                        ),
                    ],
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                        "marginLeft": "3%",
                        "minWidth": "320px",
                        "maxWidth": "420px",
                    },
                ),
            ],
            style={"width": "95%", "maxWidth": "1600px", "margin": "0 auto"},
        ),
    ],
    style={"fontFamily": "Arial, sans-serif", "padding": "10px"},
)


@app.callback(
    Output("cytoscape", "elements"),
    Output("file-info", "children"),
    Output("node-info", "children", allow_duplicate=True),  # 允许重复输出
    Output("cytoscape", "stylesheet", allow_duplicate=True),  # 允许重复输出
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    State("cytoscape", "stylesheet"),
    prevent_initial_call=True,
)
def update_output(content, filename, stylesheet):
    if content and filename.endswith(".txt"):
        import base64

        _, b64_content = content.split(",")
        decoded = base64.b64decode(b64_content).decode("utf-8")
        elements = build_graph_elements_from_text(decoded)
        # 清空节点信息和样式
        base_stylesheet = []
        for style in stylesheet:
            selector = style.get("selector", "")
            if not (
                selector.startswith("node[id =")
                or selector.startswith("edge[source =")
                or selector.startswith("edge[target =")
            ):
                base_stylesheet.append(style)
        return (
            elements,
            f"已成功上传并解析文件：{filename}",
            "请点击一个节点查看详细信息",
            base_stylesheet,
        )
    # 非txt也清空
    base_stylesheet = []
    for style in stylesheet:
        selector = style.get("selector", "")
        if not (
            selector.startswith("node[id =")
            or selector.startswith("edge[source =")
            or selector.startswith("edge[target =")
        ):
            base_stylesheet.append(style)
    return [], "❌ 文件格式错误，仅支持 .txt", "", base_stylesheet


@app.callback(
    [
        Output("node-info", "children", allow_duplicate=True),  # 允许重复输出
        Output("cytoscape", "stylesheet", allow_duplicate=True),  # 允许重复输出
    ],
    [Input("cytoscape", "tapNodeData"), Input("cytoscape", "selectedNodeData")],
    [State("cytoscape", "stylesheet"), State("cytoscape", "elements")],
    prevent_initial_call=True,
)
def handle_node_click(tap_node_data, selected_node_data, stylesheet, elements):
    # 取消选中（点击空白或取消所有节点选中）
    if not selected_node_data:
        base_stylesheet = []
        for style in stylesheet:
            selector = style.get("selector", "")
            if not (
                selector.startswith("node[id =")
                or selector.startswith("edge[source =")
                or selector.startswith("edge[target =")
            ):
                base_stylesheet.append(style)
        return "请点击一个节点查看详细信息", base_stylesheet

    # 只处理单选节点
    node_data = selected_node_data[0] if selected_node_data else None
    if not node_data:
        return "请点击一个节点查看详细信息", stylesheet

    word = node_data["label"]
    # elements 现在是最新的
    in_edges = []
    out_edges = []
    if isinstance(elements, list):
        for elem in elements:
            data = elem.get("data", {})
            if "source" in data and "target" in data:
                if data["target"] == word:
                    in_edges.append((data["source"], data.get("weight", 1)))
                elif data["source"] == word:
                    out_edges.append((data["target"], data.get("weight", 1)))

    base_stylesheet = []
    for style in stylesheet:
        selector = style.get("selector", "")
        if not (
            selector.startswith("node[id =")
            or selector.startswith("edge[source =")
            or selector.startswith("edge[target =")
        ):
            base_stylesheet.append(style)

    updated_stylesheet = base_stylesheet.copy()
    updated_stylesheet.append(
        {
            "selector": f"node[id = '{word}']",
            "style": {
                "background-color": "#4682B4",
                "border-color": "#1A5276",
                "border-width": 3,
                "text-outline-color": "#1A5276",
                "shadow-color": "#4682B4",
                "shadow-blur": 12,
                "shadow-opacity": 0.7,
                "font-size": "19px",
            },
        }
    )
    for source, _ in in_edges:
        updated_stylesheet.append(
            {
                "selector": f"edge[source = '{source}'][target = '{word}']",
                "style": {
                    "line-color": "#F39C12",
                    "target-arrow-color": "#F39C12",
                    "width": 5,
                    "opacity": 1,
                    "z-index": 999,
                    "line-style": "solid",
                    "text-background-opacity": 1,
                    "text-background-color": "#FEF5E7",
                    "text-background-shape": "round-rectangle",
                    "text-border-width": 1,
                    "text-border-color": "#F39C12",
                    "text-border-opacity": 0.8,
                    "font-size": "14px",
                    "color": "#D35400",
                    "font-weight": "bold",
                },
            }
        )
    for target, _ in out_edges:
        updated_stylesheet.append(
            {
                "selector": f"edge[source = '{word}'][target = '{target}']",
                "style": {
                    "line-color": "#00BCD4",
                    "target-arrow-color": "#00BCD4",
                    "width": 5,
                    "opacity": 1,
                    "z-index": 999,
                    "line-style": "solid",
                    "arrow-scale": 1.5,
                    "text-background-opacity": 1,
                    "text-background-color": "#E0F7FA",
                    "text-background-shape": "round-rectangle",
                    "text-border-width": 1,
                    "text-border-color": "#00BCD4",
                    "text-border-opacity": 0.8,
                    "font-size": "14px",
                    "color": "#0097A7",
                    "font-weight": "bold",
                },
            }
        )

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
    return info_components, updated_stylesheet


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


if __name__ == "__main__":
    app.run(debug=True)
