from dash import html

# 统一定义消息标题样式
TITLE_STYLE = {"color": "#0077B6", "marginBottom": "8px", "marginTop": "0"}
SUBTITLE_STYLE = {
    "color": "#444",
    "marginBottom": "6px",
    "marginTop": "10px",
    "fontSize": "16px",
}

# 统一定义消息文本样式
INFO_TEXT_STYLE = {"fontWeight": "bold", "color": "#666", "marginBottom": "5px"}
BRIDGE_RESULT_STYLE = {
    "fontWeight": "bold",
    "color": "#ff8f00",
    "padding": "8px",
    "backgroundColor": "#fff8e1",
    "borderRadius": "4px",
}
SHORTEST_PATH_RESULT_STYLE = {
    "fontWeight": "bold",
    "color": "#7b1fa2",
    "padding": "8px",
    "backgroundColor": "#f3e5f5",
    "borderRadius": "4px",
}
HELP_TEXT_STYLE = {
    "fontStyle": "italic",
    "color": "#666",
    "fontSize": "14px",
    "marginTop": "8px",
}
WARNING_TEXT_STYLE = {
    "fontWeight": "bold",
    "color": "#e53935",
    "padding": "8px",
    "backgroundColor": "#ffebee",
    "borderRadius": "4px",
}
RANDOM_WALK_ACTIVE_STYLE = {"fontWeight": "bold", "color": "#9c27b0"}
RANDOM_WALK_ERROR_STYLE = {"color": "#e53935"}

# 统一卡片容器样式
CARD_STYLE = {
    "backgroundColor": "white",
    "borderRadius": "4px",
    "padding": "12px",
    "marginBottom": "10px",
    "boxShadow": "0 1px 3px rgba(0,0,0,0.12)",
}

# 分隔线样式
DIVIDER_STYLE = {"margin": "8px 0", "borderTop": "1px solid #eee"}


def welcome_message():
    """返回欢迎信息组件"""
    return [
        html.H4("欢迎使用词图可视化工具", style=TITLE_STYLE),
        html.Hr(style=DIVIDER_STYLE),
        html.Div(
            [
                html.P(
                    "请点击一个节点查看详细信息或选择两个节点查询桥接词/最短路径",
                    style=INFO_TEXT_STYLE,
                ),
            ],
            style=CARD_STYLE,
        ),
        html.P("选择模式后可进行相应查询，或启动随机游走", style=HELP_TEXT_STYLE),
    ]


def warning_message(
    message="请只选择一个节点查看详情或选择恰好两个节点查询桥接词/最短路径",
):
    """返回警告信息组件"""
    return [
        html.H4("选择提示", style=TITLE_STYLE),
        html.Hr(style=DIVIDER_STYLE),
        html.Div(
            [
                html.P(message, style=WARNING_TEXT_STYLE),
            ],
            style=CARD_STYLE,
        ),
        html.P("请清除部分选择后重试", style=HELP_TEXT_STYLE),
    ]


def node_info_message(word, in_edges, out_edges):
    """返回节点详细信息组件"""
    return [
        html.H4(f"单词: {word}", style=TITLE_STYLE),
        html.Hr(style=DIVIDER_STYLE),
        html.Div(
            [
                html.H5("入边 (前驱词):", style=SUBTITLE_STYLE),
                (
                    html.Ul(
                        [
                            html.Li(
                                f"{source} → {word} (权重: {weight})",
                                style={"marginBottom": "3px"},
                            )
                            for source, weight in sorted(in_edges, key=lambda x: -x[1])
                        ],
                        style={
                            "paddingLeft": "20px",
                            "marginBottom": "8px",
                            "marginTop": "5px",
                        },
                    )
                    if in_edges
                    else html.P(
                        "无入边", style={"fontStyle": "italic", "color": "#666"}
                    )
                ),
            ],
            style=CARD_STYLE,
        ),
        html.Div(
            [
                html.H5("出边 (后继词):", style=SUBTITLE_STYLE),
                (
                    html.Ul(
                        [
                            html.Li(
                                f"{word} → {target} (权重: {weight})",
                                style={"marginBottom": "3px"},
                            )
                            for target, weight in sorted(out_edges, key=lambda x: -x[1])
                        ],
                        style={
                            "paddingLeft": "20px",
                            "marginBottom": "8px",
                            "marginTop": "5px",
                        },
                    )
                    if out_edges
                    else html.P(
                        "无出边", style={"fontStyle": "italic", "color": "#666"}
                    )
                ),
            ],
            style=CARD_STYLE,
        ),
        html.Div(
            [
                html.H5("统计:", style=SUBTITLE_STYLE),
                html.Div(
                    [
                        html.Span(f"总前驱单词数: ", style={"fontWeight": "bold"}),
                        html.Span(f"{len(in_edges)}", style={"color": "#0288d1"}),
                    ],
                    style={"marginBottom": "5px"},
                ),
                html.Div(
                    [
                        html.Span(f"总后继单词数: ", style={"fontWeight": "bold"}),
                        html.Span(f"{len(out_edges)}", style={"color": "#0288d1"}),
                    ],
                    style={"marginBottom": "5px"},
                ),
                html.Div(
                    [
                        html.Span(f"总关联单词数: ", style={"fontWeight": "bold"}),
                        html.Span(
                            f"{len(in_edges) + len(out_edges)}",
                            style={"color": "#0288d1"},
                        ),
                    ]
                ),
            ],
            style=CARD_STYLE,
        ),
    ]


def bridge_result_message(msg_text):
    """返回桥接词查询结果组件"""
    return [
        html.H4("桥接词查询结果", style=TITLE_STYLE),
        html.Hr(style=DIVIDER_STYLE),
        html.Div(
            [
                html.P(msg_text, style=BRIDGE_RESULT_STYLE),
            ],
            style=CARD_STYLE,
        ),
        html.P("请点击节点查看详细信息，或继续查询", style=HELP_TEXT_STYLE),
    ]


def shortest_path_result_message(msg_text):
    """返回最短路径查询结果组件"""
    return [
        html.H4("最短路径查询结果", style=TITLE_STYLE),
        html.Hr(style=DIVIDER_STYLE),
        html.Div(
            [
                html.P(msg_text, style=SHORTEST_PATH_RESULT_STYLE),
            ],
            style=CARD_STYLE,
        ),
        html.P("请点击节点查看详细信息，或继续查询", style=HELP_TEXT_STYLE),
    ]


def random_walk_result_message(walked_nodes, walked_edges, stop_reason):
    """返回随机游走结果组件"""
    steps = []
    for i, (src, tgt, weight) in enumerate(walked_edges):
        steps.append(
            html.Li(
                [
                    f"Step {i+1}: ",
                    html.Span(
                        f"{src} → {tgt}",
                        style={"fontWeight": "bold", "color": "#0288d1"},
                    ),
                    f" (权重: {weight})",
                ],
                style={"marginBottom": "2px"},
            )
        )

    is_error = "遇到重复边" in stop_reason or "没有出边" in stop_reason
    status_style = RANDOM_WALK_ERROR_STYLE if is_error else RANDOM_WALK_ACTIVE_STYLE

    return [
        html.H4("随机游走结果", style=TITLE_STYLE),
        html.Hr(style=DIVIDER_STYLE),
        html.Div(
            [
                html.Div(
                    [
                        html.Span(
                            "起点: ", style={"fontWeight": "bold", **SUBTITLE_STYLE}
                        ),
                        html.Span(
                            walked_nodes[0] if walked_nodes else "无",
                            style={"fontWeight": "bold", "color": "#388e3c"},
                        ),
                    ],
                    style={"marginBottom": "8px"},
                ),
                html.Div(
                    [
                        html.Span(
                            "当前节点: ", style={"fontWeight": "bold", **SUBTITLE_STYLE}
                        ),
                        html.Span(
                            walked_nodes[-1] if walked_nodes else "无",
                            style=RANDOM_WALK_ACTIVE_STYLE,
                        ),
                    ],
                    style={"marginBottom": "8px"},
                ),
                html.Div(
                    [
                        html.Span(
                            "状态: ", style={"fontWeight": "bold", **SUBTITLE_STYLE}
                        ),
                        html.Span(stop_reason, style=status_style),
                    ],
                    style={"marginBottom": "8px"},
                ),
            ],
            style=CARD_STYLE,
        ),
        html.Div(
            [
                html.H5("统计:", style=SUBTITLE_STYLE),
                html.Div(
                    [
                        html.Span(f"当前步数: ", style={"fontWeight": "bold"}),
                        html.Span(f"{len(walked_edges)}", style={"color": "#0277bd"}),
                    ],
                    style={"marginBottom": "5px"},
                ),
                html.Div(
                    [
                        html.Span(f"已访问节点数: ", style={"fontWeight": "bold"}),
                        html.Span(
                            f"{len(set(walked_nodes))}", style={"color": "#0277bd"}
                        ),
                    ]
                ),
            ],
            style=CARD_STYLE,
        ),
        html.Div(
            [
                html.H5("游走路径:", style=SUBTITLE_STYLE),
                (
                    html.Ul(
                        steps,
                        style={
                            "maxHeight": "210px",
                            "overflowY": "auto",
                            "paddingLeft": "20px",
                            "marginTop": "5px",
                        },
                    )
                    if steps
                    else html.P(
                        "无游走路径", style={"fontStyle": "italic", "color": "#666"}
                    )
                ),
            ],
            style=CARD_STYLE,
        ),
    ]
