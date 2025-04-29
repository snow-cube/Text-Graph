import sys
import dash
from dash import html, dcc, Input, Output, State
import dash_cytoscape as cyto
from text_graph import TextGraph
from style_utils import get_base_stylesheet
from register_callbacks import register_callbacks
from callbacks.upload import NODE_THRESHOLD

# ==== 启动时检查是否提供文件路径 ====
initial_text = ""
initial_locked = False
if len(sys.argv) == 2:
    try:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            initial_text = f.read()
            # 检查初始数据的节点数
            if initial_text:
                text_graph = TextGraph(initial_text)
                if len(text_graph.nodes) > NODE_THRESHOLD:
                    initial_locked = True
    except Exception as e:
        print(f"⚠️ 无法读取文件: {e}")

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "词图可视化"

app.layout = html.Div(
    [
        html.H2(
            "词图可视化工具（有向图）",
            style={"textAlign": "center", "margin": "20px 0"},
        ),
        # 新增：将 style-store 移到布局顶层，确保始终存在
        dcc.Store(
            id="style-store",
            data={
                "selected_nodes": [],
                "bridge_words": [],
                "highlighted_edges": [],
                "base_style_applied": True,
            },
        ),
        html.Div(
            [
                html.Div(
                    [
                        # 新增：图显示控制开关
                        html.Div(
                            [
                                dcc.Checklist(
                                    id="graph-display-toggle",
                                    options=[
                                        {"label": " 显示图形可视化", "value": "show"}
                                    ],
                                    value=(
                                        [] if initial_locked else ["show"]
                                    ),  # 根据初始锁定状态设置默认值
                                    style={
                                        "fontWeight": "bold",
                                        "marginBottom": "10px",
                                    },
                                ),
                            ],
                        ),
                        # 新增：存储图显示状态
                        dcc.Store(
                            id="graph-display-state",
                            data={"show": not initial_locked, "locked": initial_locked},
                        ),
                        # 修改：空的图组件容器，内容通过回调动态控制
                        html.Div(
                            id="graph-container",
                            style={
                                "position": "relative",
                                "width": "100%",
                                "height": "700px",
                                "marginBottom": "10px",
                            },
                        ),
                        # 新增：用于存储图对象的序列化数据
                        dcc.Store(
                            id="graph-store",
                            data=initial_text if initial_text else "",
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
                                # 移除保存为图片按钮 - 将在图内部显示
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
                            "桥接词/最短路查询",
                            style={
                                "textAlign": "center",
                                "marginTop": "18px",
                                "marginBottom": "10px",
                                "color": "#0077B6",
                                "fontWeight": "bold",
                                "letterSpacing": "2px",
                            },
                        ),
                        # 新增：模式切换控件
                        html.Div(
                            [
                                dcc.RadioItems(
                                    id="query-mode-switch",
                                    options=[
                                        {"label": "桥接词", "value": "bridge"},
                                        {"label": "最短路", "value": "shortest"},
                                    ],
                                    value="bridge",
                                    labelStyle={
                                        "display": "inline-block",
                                        "marginRight": "18px",
                                        "fontSize": "16px",
                                    },
                                    style={
                                        "marginBottom": "10px",
                                        "textAlign": "center",
                                    },
                                ),
                            ],
                            style={"textAlign": "center", "marginBottom": "8px"},
                        ),
                        html.Div(
                            [
                                dcc.Input(
                                    id="bridge-word1",
                                    type="text",
                                    placeholder="单词1",
                                    style={"width": "40%", "marginRight": "8px"},
                                ),
                                dcc.Input(
                                    id="bridge-word2",
                                    type="text",
                                    placeholder="单词2",
                                    style={"width": "40%", "marginRight": "8px"},
                                ),
                                html.Button(
                                    id="bridge-shortest-query-btn",
                                    n_clicks=0,
                                    children="查询",
                                    style={
                                        "fontSize": "15px",
                                        "padding": "6px 16px",
                                        "backgroundColor": "#43a047",
                                        "color": "#fff",
                                        "border": "none",
                                        "borderRadius": "4px",
                                        "cursor": "pointer",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justifyContent": "center",
                                "alignItems": "center",
                                "gap": "8px",
                                "marginBottom": "10px",
                            },
                        ),
                        html.Div(
                            id="bridge-result",
                            style={
                                "border": "1px solid #b7e4c7",
                                "backgroundColor": "#f1f8e9",
                                "borderRadius": "5px",
                                "padding": "10px",
                                "marginBottom": "18px",
                                "minHeight": "36px",
                                "color": "#388e3c",
                                "fontSize": "15px",
                                "textAlign": "center",
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


# 重构回调：处理图形显示锁定和切换
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
    reset_style = {
        "selected_nodes": [],
        "bridge_words": [],
        "highlighted_edges": [],
        "base_style_applied": True,
    }

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


register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
