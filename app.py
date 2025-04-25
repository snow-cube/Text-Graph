import sys
import dash
from dash import html, dcc
import dash_cytoscape as cyto
from text_graph import TextGraph
from style_utils import get_base_stylesheet
from register_callbacks import register_callbacks

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
                        # 新增：相对定位容器包裹 Cytoscape 和按钮
                        html.Div(
                            [
                                cyto.Cytoscape(
                                    id="cytoscape",
                                    elements=(
                                        TextGraph(initial_text).get_elements()
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
                                    stylesheet=get_base_stylesheet(),
                                ),
                                # 新增：清空所有选中按钮，绝对定位在 Cytoscape 右上角
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
                            ],
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
                            data=TextGraph(initial_text).text if initial_text else "",
                        ),
                        # 新增：用于管理样式状态的存储组件
                        dcc.Store(
                            id="style-store",
                            data={
                                "selected_nodes": [],
                                "bridge_words": [],
                                "highlighted_edges": [],
                                "base_style_applied": True,
                            },
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
                                    id="bridge-query-btn",
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

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
