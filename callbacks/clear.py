from dash import Output, Input
import dash
from layouts.message_templates import welcome_message
from styles.basic_styles import get_reset_style_state


def register_clear_callback(app):
    @app.callback(
        Output("style-store", "data", allow_duplicate=True),
        Output("node-info", "children", allow_duplicate=True),
        Output("bridge-word1", "value", allow_duplicate=True),
        Output("bridge-word2", "value", allow_duplicate=True),
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
            )
        style_state = get_reset_style_state()
        # 使用欢迎信息模板
        return (
            style_state,
            welcome_message(),
            "",
            "",
        )
