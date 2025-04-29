from dash import Output, Input, State
from text_graph import TextGraph

# 设置节点阈值，超过此阈值将锁定图形显示
NODE_THRESHOLD = 100

def register_upload_callback(app):
    @app.callback(
        Output("graph-store", "data"),
        Output("file-info", "children"),
        Output("node-info", "children", allow_duplicate=True),
        Output("graph-display-state", "data", allow_duplicate=True),
        Input("upload-data", "contents"),
        State("upload-data", "filename"),
        State("graph-display-state", "data"),
        prevent_initial_call=True,
    )
    def update_output(content, filename, display_state):
        if content and filename.endswith(".txt"):
            import base64

            _, b64_content = content.split(",")
            decoded = base64.b64decode(b64_content).decode("utf-8")

            # 检查图的节点数量
            text_graph = TextGraph(decoded)
            node_count = len(text_graph.nodes)

            # 更新状态并标记数据已更新
            display_state["data_updated"] = True

            # 如果节点数量超过阈值，锁定图形显示
            if node_count > NODE_THRESHOLD:
                display_state["locked"] = True
                display_state["show"] = False
                file_info = f"已成功上传并解析文件：{filename} (节点数: {node_count}, 已锁定图形显示)"
            else:
                display_state["locked"] = False
                file_info = f"已成功上传并解析文件：{filename} (节点数: {node_count})"

            return (
                decoded,  # Store the text data in graph-store
                file_info,
                "请点击一个节点查看详细信息",
                display_state,
            )

        # Add a flag to indicate there was an error
        display_state["data_updated"] = False

        return "", "❌ 文件格式错误，仅支持 .txt", "", display_state
