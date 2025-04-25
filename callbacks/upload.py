from dash import Output, Input, State
from text_graph import TextGraph


def register_upload_callback(app):
    @app.callback(
        Output("cytoscape", "elements"),
        Output("file-info", "children"),
        Output("node-info", "children", allow_duplicate=True),
        Output("style-store", "data"),
        Output("graph-store", "data"),
        Input("upload-data", "contents"),
        State("upload-data", "filename"),
        State("style-store", "data"),
        prevent_initial_call=True,
    )
    def update_output(content, filename, style_state):
        if content and filename.endswith(".txt"):
            import base64

            _, b64_content = content.split(",")
            decoded = base64.b64decode(b64_content).decode("utf-8")
            tg = TextGraph(decoded)
            elements = tg.get_elements()
            style_state = {
                "selected_nodes": [],
                "bridge_words": [],
                "highlighted_edges": [],
                "base_style_applied": True,
            }
            return (
                elements,
                f"已成功上传并解析文件：{filename}",
                "请点击一个节点查看详细信息",
                style_state,
                decoded,
            )
        style_state = {
            "selected_nodes": [],
            "bridge_words": [],
            "highlighted_edges": [],
            "base_style_applied": True,
        }
        return [], "❌ 文件格式错误，仅支持 .txt", "", style_state, ""
