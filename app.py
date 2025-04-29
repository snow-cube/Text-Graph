import sys
import dash
from dash import html, dcc
from text_graph import TextGraph
from styles.basic_style import get_reset_style_state
from register_callbacks import register_callbacks
from callbacks.upload import NODE_THRESHOLD
from message_templates import welcome_message

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
                if text_graph.node_count > NODE_THRESHOLD:
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
            data=get_reset_style_state(),
        ),
        # 新增：随机游走状态存储
        dcc.Store(id="random-walk-store", data={}),
        # 新增：PageRank 结果存储
        dcc.Store(id="pagerank-store", data={}),
        # 新增：用于控制随机游走步进的间隔计时器
        dcc.Interval(
            id="random-walk-interval",
            interval=500,  # 每 500 毫秒更新一次，可以根据需要调整
            n_intervals=0,
            disabled=True,
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
                                    disabled=False,  # 添加初始disabled属性
                                ),
                                dcc.Input(
                                    id="bridge-word2",
                                    type="text",
                                    placeholder="单词2",
                                    style={"width": "40%", "marginRight": "8px"},
                                    disabled=False,  # 添加初始disabled属性
                                ),
                                html.Button(
                                    id="bridge-shortest-query-btn",
                                    n_clicks=0,
                                    children="查询",
                                    disabled=False,  # 添加初始disabled属性
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
                                "marginBottom": "20px",  # 增加底部间距
                            },
                        ),
                        # 新增：单节点查询区域
                        html.H3(
                            "节点信息查询",
                            style={
                                "textAlign": "center",
                                "marginTop": "18px",
                                "marginBottom": "10px",
                                "color": "#0077B6",
                                "fontWeight": "bold",
                                "letterSpacing": "2px",
                            },
                        ),
                        html.Div(
                            [
                                dcc.Input(
                                    id="node-query-input",
                                    type="text",
                                    placeholder="输入节点名称",
                                    style={"width": "70%", "marginRight": "8px"},
                                    disabled=False,
                                ),
                                html.Button(
                                    id="node-query-btn",
                                    n_clicks=0,
                                    children="查询",
                                    disabled=False,
                                    style={
                                        "fontSize": "15px",
                                        "padding": "6px 16px",
                                        "backgroundColor": "#2196F3",
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
                                "marginBottom": "20px",
                            },
                        ),
                        # 删除 bridge-result div，将结果合并到 node-info
                        # 注意：node-info 的标题修改为更加通用的名称
                        html.H3(
                            "节点与查询信息",  # 修改标题为更通用的名称
                            style={
                                "textAlign": "center",
                                "marginTop": "0px",
                                "marginBottom": "10px",
                                "color": "#0077B6",
                                "fontWeight": "bold",
                                "letterSpacing": "2px",
                            },
                        ),
                        # 添加随机游走按钮和容器
                        html.Div(
                            [
                                # 按钮行容器 - 将开始、停止和保存按钮排成一行
                                html.Div(
                                    [
                                        html.Button(
                                            "开始随机游走",
                                            id="random-walk-btn",
                                            n_clicks=0,
                                            style={
                                                "fontSize": "15px",
                                                "padding": "7px 10px",
                                                "backgroundColor": "#9c27b0",
                                                "color": "#fff",
                                                "border": "none",
                                                "borderRadius": "4px",
                                                "cursor": "pointer",
                                                "flex": "1",
                                            },
                                        ),
                                        html.Button(
                                            "停止随机游走",
                                            id="stop-walk-btn",
                                            n_clicks=0,
                                            style={
                                                "display": "none",  # 初始隐藏
                                                "fontSize": "15px",
                                                "padding": "7px 10px",
                                                "backgroundColor": "#e53935",
                                                "color": "#fff",
                                                "border": "none",
                                                "borderRadius": "4px",
                                                "cursor": "pointer",
                                                "flex": "1",
                                            },
                                        ),
                                        html.Button(
                                            "保存游走单词序列",
                                            id="save-walk-btn",
                                            n_clicks=0,
                                            style={
                                                "fontSize": "15px",
                                                "padding": "7px 10px",
                                                "backgroundColor": "#aaaaaa",  # 初始为灰色（禁用状态）
                                                "color": "#fff",
                                                "border": "none",
                                                "borderRadius": "4px",
                                                "cursor": "not-allowed",  # 初始禁用
                                                "flex": "1",
                                                "marginLeft": "10px",
                                            },
                                            disabled=True,  # 初始禁用
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "flexDirection": "row",
                                        "marginTop": "10px",
                                        "width": "100%",
                                    },
                                ),
                                # 添加下载组件
                                dcc.Download(id="download-walk-sequence"),
                            ],
                            id="random-walk-container",
                            style={"marginBottom": "10px"},
                        ),
                        # 添加PageRank计算选项
                        html.Div(
                            [
                                dcc.Checklist(
                                    id="pagerank-toggle",
                                    options=[
                                        {
                                            "label": " 开启PageRank计算",
                                            "value": "enabled",
                                        }
                                    ],
                                    value=[],
                                    style={
                                        "marginBottom": "10px",
                                        "fontWeight": "bold",
                                    },
                                ),
                            ],
                            style={"marginBottom": "10px"},
                        ),
                        html.Div(
                            id="node-info",
                            children=welcome_message(),  # 设置初始欢迎信息
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
