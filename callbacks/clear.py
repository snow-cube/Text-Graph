from dash import Output, Input
import dash


def register_clear_callback(app):
    @app.callback(
        Output("style-store", "data", allow_duplicate=True),
        Output("node-info", "children", allow_duplicate=True),
        Output("bridge-word1", "value", allow_duplicate=True),
        Output("bridge-word2", "value", allow_duplicate=True),
        Output("bridge-result", "children", allow_duplicate=True),
        Input("clear-selection-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def clear_selection(n_clicks):
        if not n_clicks:
            return (
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )
        style_state = {
            "selected_nodes": [],
            "bridge_words": [],
            "highlighted_edges": [],
            "base_style_applied": True,
        }
        return (
            style_state,
            "请点击一个节点查看详细信息或选择两个节点查询桥接词",
            "",
            "",
            "",
        )
