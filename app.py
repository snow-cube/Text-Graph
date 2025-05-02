import sys
import os
import dash
from dash import html, dcc
from layouts.module_container import container_line, module_container
from text_graph import TextGraph
from styles.basic_styles import get_reset_style_state
from styles.button_input_styles import (
    RANDOM_WALK_START_BUTTON_STYLE,
    get_query_button_style,
    get_node_query_button_style,
    get_save_walk_button_style,
    get_bridge_text_button_style,
    get_input_style,
    get_textarea_style,
)
from register_callbacks import register_callbacks
from callbacks.upload import NODE_THRESHOLD
from layouts.message_templates import welcome_message
from layouts.module_container import MODULE_CONTAINER_STYLE

# ==== 启动时检查是否提供文件路径 ====
initial_text = ""
initial_locked = False
initial_filename = ""  # 添加保存初始文件名
if len(sys.argv) == 2:
    try:
        filepath = sys.argv[1]
        with open(filepath, "r", encoding="utf-8") as f:
            initial_text = f.read()
            initial_filename = os.path.basename(filepath)
            # 检查初始数据的节点数
            if initial_text:
                text_graph = TextGraph(initial_text)
                initial_node_count = text_graph.node_count  # 保存节点数量
                if text_graph.node_count > NODE_THRESHOLD:
                    initial_locked = True
    except Exception as e:
        print(f"⚠️ 无法读取文件: {e}")

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "词图可视化"

app.layout = html.Div(
    [
        # 添加浮动通知组件
        html.Div(
            id="toast-notification",
            children=[],
            style={
                "position": "fixed",
                "top": "20px",
                "right": "20px",
                "zIndex": "1000",
                "minWidth": "250px",
                "maxWidth": "400px",
                "transform": "translateX(420px)",  # 初始状态在屏幕外
                "transition": "transform 0.5s ease-in-out, opacity 0.5s ease-in-out",
                "opacity": "0",
                "boxShadow": "0 4px 8px rgba(0,0,0,0.2)",
                "borderRadius": "4px",
            },
        ),
        # 添加控制通知显示时间的计时器
        dcc.Interval(
            id="toast-interval",
            interval=6000,  # 6 秒后触发
            n_intervals=0,
            max_intervals=1,
            disabled=True,
        ),
        # 存储通知状态
        dcc.Store(id="toast-state", data={"visible": False}),
        # 移除原有的标题栏，其他状态存储保持不变
        dcc.Store(
            id="style-store",
            data=get_reset_style_state(),
        ),
        dcc.Store(id="random-walk-store", data={}),
        dcc.Store(id="pagerank-store", data={}),
        dcc.Store(
            id="ui-state-store",
            data={
                "walk_active": False,  # 是否正在随机游走
                "save_enabled": False,  # 是否可以保存游走结果
                "query_enabled": True,  # 是否启用查询功能
            },
        ),
        dcc.Interval(
            id="random-walk-interval",
            interval=300,  # 每 300 毫秒更新一次，可以根据需要调整
            n_intervals=0,
            disabled=True,
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                # 左侧：图显示控制开关
                                html.Div(
                                    dcc.Checklist(
                                        id="graph-display-toggle",
                                        options=[
                                            {
                                                "label": " 显示图形可视化",
                                                "value": "show",
                                            }
                                        ],
                                        value=(
                                            [] if initial_locked else ["show"]
                                        ),  # 根据初始锁定状态设置默认值
                                        style={
                                            "fontWeight": "bold",
                                        },
                                    ),
                                    style={
                                        "flex": "0 0 auto",
                                        "paddingRight": "15px",
                                        "marginLeft": "18px",
                                    },
                                ),
                                # 中间：文件信息
                                html.Div(
                                    id="header-file-info",
                                    children=initial_filename
                                    and f"当前文件: {initial_filename} ({initial_node_count} 个节点)"
                                    or "",
                                    style={
                                        "color": "#2E7D32",
                                        "fontWeight": "500",
                                        "fontSize": "14px",
                                        "whiteSpace": "nowrap",
                                        "overflow": "hidden",
                                        "textOverflow": "ellipsis",
                                        "flex": "1",
                                        "textAlign": "center",
                                    },
                                ),
                                # 右侧：上传按钮
                                dcc.Upload(
                                    id="upload-data",
                                    children=html.Button(
                                        "上传文本文件",
                                        style={
                                            "fontSize": "14px",
                                            "padding": "6px 14px",
                                            "marginRight": "18px",
                                            "backgroundColor": "#00A8E8",
                                            "color": "#fff",
                                            "border": "none",
                                            "borderRadius": "4px",
                                            "cursor": "pointer",
                                            "whiteSpace": "nowrap",
                                        },
                                    ),
                                    accept=".txt",
                                    multiple=False,
                                    style={"flex": "0 0 auto"},
                                ),
                            ],
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "marginBottom": "15px",
                                "backgroundColor": "#f9f9f9",
                                "padding": "10px 0",
                                "border": "1px solid #ddd",
                                "borderRadius": "8px",
                                "boxShadow": "0 1px 3px rgba(0,0,0,0.08)",
                                "width": "100%",
                            },
                        ),
                        # 存储图显示状态
                        dcc.Store(
                            id="graph-display-state",
                            data={"show": not initial_locked, "locked": initial_locked},
                        ),
                        # 图组件容器
                        html.Div(
                            id="graph-container",
                            style={
                                "position": "relative",
                                "width": "100%",
                                # "height": "700px",
                                "height": "calc(100vh - 125px)",
                                "minHeight": "320px",
                                "marginBottom": "10px",
                            },
                        ),
                        # 用于存储图对象的序列化数据
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
                        module_container(
                            title="桥接词/最短路查询",
                            content_list=[
                                container_line(
                                    [
                                        dcc.Input(
                                            id="bridge-word1",
                                            type="text",
                                            placeholder="单词 1",
                                            style=get_input_style(width="40%"),
                                            disabled=False,
                                        ),
                                        dcc.Input(
                                            id="bridge-word2",
                                            type="text",
                                            placeholder="单词 2",
                                            style=get_input_style(width="40%"),
                                            disabled=False,
                                        ),
                                        html.Button(
                                            id="bridge-shortest-query-btn",
                                            n_clicks=0,
                                            children="查询",
                                            disabled=False,
                                            style=get_query_button_style(enabled=True),
                                        ),
                                    ]
                                )
                            ],
                            right_component=dcc.RadioItems(
                                id="query-mode-switch",
                                options=[
                                    {
                                        "label": "桥接词",
                                        "value": "bridge",
                                    },
                                    {
                                        "label": "最短路",
                                        "value": "shortest",
                                    },
                                ],
                                value="bridge",
                                labelStyle={
                                    "display": "inline-block",
                                    "marginLeft": "10px",
                                    "fontWeight": "bold",
                                    "fontSize": "14px",
                                },
                                style={
                                    "display": "inline-block",
                                },
                            ),
                        ),
                        module_container(
                            title="节点信息查询",
                            content_list=[
                                container_line(
                                    [
                                        dcc.Input(
                                            id="node-query-input",
                                            type="text",
                                            placeholder="输入节点名称",
                                            style=get_input_style(width="100%"),
                                            disabled=False,
                                        ),
                                        html.Button(
                                            id="node-query-btn",
                                            n_clicks=0,
                                            children="查询",
                                            disabled=False,
                                            style=get_node_query_button_style(
                                                enabled=True
                                            ),
                                        ),
                                    ]
                                )
                            ],
                            right_component=dcc.Checklist(
                                id="pagerank-toggle",
                                options=[
                                    {
                                        "label": "开启 PageRank 计算",
                                        "value": "enabled",
                                    },
                                ],
                                value=[],
                                style={
                                    "fontWeight": "bold",
                                    "fontSize": "14px",
                                    "display": "inline-block",
                                },
                            ),
                        ),
                        module_container(
                            title="随机游走",
                            content_list=[
                                container_line(
                                    [
                                        html.Button(
                                            "开始随机游走",
                                            id="random-walk-btn",
                                            n_clicks=0,
                                            style=RANDOM_WALK_START_BUTTON_STYLE,
                                        ),
                                        html.Button(
                                            "停止随机游走",
                                            id="stop-walk-btn",
                                            n_clicks=0,
                                            style={"display": "none"},  # 初始隐藏
                                        ),
                                        html.Button(
                                            "保存游走单词序列",
                                            id="save-walk-btn",
                                            n_clicks=0,
                                            style=get_save_walk_button_style(
                                                enabled=False
                                            ),
                                            disabled=True,  # 初始禁用
                                        ),
                                    ]
                                ),
                                dcc.Download(id="download-walk-sequence"),
                            ],
                        ),
                        module_container(
                            title="文本桥接生成",
                            content_list=[
                                container_line(
                                    [
                                        dcc.Textarea(
                                            id="bridge-text-input",
                                            placeholder="输入文本，将自动插入桥接词...",
                                            style=get_textarea_style(),
                                        ),
                                        html.Button(
                                            id="generate-bridge-text-btn",
                                            n_clicks=0,
                                            children="生成",
                                            disabled=False,
                                            style=get_bridge_text_button_style(
                                                enabled=True
                                            ),
                                        ),
                                    ]
                                )
                            ],
                        ),
                        # 结果显示区域
                        html.Div(
                            id="node-info",
                            children=welcome_message(),
                            style={
                                **MODULE_CONTAINER_STYLE,
                                "flex": "1",
                                "minHeight": "200px",
                                "height": "calc(100vh - 550px)",
                                "overflowY": "auto",
                            },
                        ),
                    ],
                    style={
                        "width": "30%",
                        "height": "calc(100vh - 70px)",
                        "minHeight": "375px",
                        "display": "inline-block",
                        "verticalAlign": "top",
                        "marginLeft": "3%",
                        "minWidth": "320px",
                        "maxWidth": "420px",
                        "padding": "12px 12px 0 12px",
                        "borderRadius": "8px",
                        "boxShadow": "0 1px 4px #e0e0e0",
                        "overflowY": "auto",
                    },
                ),
            ],
            style={"width": "95%", "maxWidth": "1600px", "margin": "0 auto"},
        ),
    ],
    style={"fontFamily": "Arial, sans-serif", "padding": "20px 10px 10px 10px"},
)

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
