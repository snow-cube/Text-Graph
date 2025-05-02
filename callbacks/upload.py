from dash import Output, Input, State, html
from text_graph import TextGraph

# 设置节点阈值，超过此阈值将锁定图形显示
NODE_THRESHOLD = 100


def register_upload_callback(app):
    @app.callback(
        Output("graph-store", "data"),
        Output("header-file-info", "children"),  # 更新标题栏文件信息
        Output("node-info", "children", allow_duplicate=True),
        Output("graph-display-state", "data", allow_duplicate=True),
        # Toast通知相关输出
        Output("toast-notification", "children", allow_duplicate=True),
        Output("toast-notification", "style", allow_duplicate=True),
        Output("toast-interval", "disabled", allow_duplicate=True),
        Output("toast-state", "data", allow_duplicate=True),
        Input("upload-data", "contents"),
        State("upload-data", "filename"),
        State("graph-display-state", "data"),
        State("toast-notification", "style"),
        prevent_initial_call=True,
    )
    def update_output(content, filename, display_state, toast_style):
        # 创建 Toast 显示样式
        visible_toast_style = dict(toast_style)
        visible_toast_style["transform"] = "translateX(0)"
        visible_toast_style["opacity"] = "1"

        if content and filename.endswith(".txt"):
            import base64

            _, b64_content = content.split(",")
            decoded = base64.b64decode(b64_content).decode("utf-8")

            # 检查图的节点数量
            node_count = TextGraph(decoded).node_count

            # 更新状态并标记数据已更新
            display_state["data_updated"] = True

            # 如果节点数量超过阈值，锁定图形显示
            if node_count > NODE_THRESHOLD:
                display_state["locked"] = True
                display_state["show"] = False
                file_info = (
                    f"当前文件: {filename} ({node_count} 个节点, 图形显示已锁定)"
                )
                toast_message = (
                    f"✓ 已成功上传：{filename} ({node_count} 个节点, 已锁定图形显示)"
                )
                toast_bg_color = "#4CAF50"
            else:
                display_state["locked"] = False
                file_info = f"当前文件: {filename} ({node_count} 个节点)"
                toast_message = f"✓ 已成功上传：{filename} ({node_count} 个节点)"
                toast_bg_color = "#4CAF50"

            # 创建 Toast 内容
            toast_content = html.Div(
                html.P(
                    toast_message,
                    style={
                        "backgroundColor": toast_bg_color,
                        "color": "white",
                        "padding": "15px",
                        "borderRadius": "4px",
                        "margin": "0",
                        "fontSize": "15px",
                    },
                )
            )

            return (
                decoded,  # Store the text data in graph-store
                file_info,  # 更新标题栏文件信息
                "请点击一个节点查看详细信息",
                display_state,
                toast_content,  # Toast 内容
                visible_toast_style,  # Toast 样式
                False,  # 启用计时器
                {"visible": True},  # 更新通知状态
            )

        # 处理错误情况
        toast_content = html.Div(
            html.P(
                "❌ 文件格式错误，仅支持 .txt",
                style={
                    "backgroundColor": "#F44336",
                    "color": "white",
                    "padding": "15px",
                    "borderRadius": "4px",
                    "margin": "0",
                    "fontSize": "15px",
                },
            )
        )

        return (
            "",
            "未选择有效文件",  # 错误情况下的标题栏文件信息
            "",
            display_state,
            toast_content,  # Toast 错误内容
            visible_toast_style,  # Toast 样式
            False,  # 启用计时器
            {"visible": True},  # 更新通知状态
        )
