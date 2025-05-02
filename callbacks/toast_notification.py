from dash import Output, Input, State
from dash.exceptions import PreventUpdate


def register_toast_callback(app):
    """注册 Toast 通知回调 - 控制通知自动隐藏"""

    @app.callback(
        Output("toast-notification", "style", allow_duplicate=True),
        Output("toast-interval", "disabled", allow_duplicate=True),
        Output(
            "toast-interval", "n_intervals", allow_duplicate=True
        ),  # 添加重置计数器的输出
        Output("toast-state", "data", allow_duplicate=True),  # 添加更新状态的输出
        Input("toast-interval", "n_intervals"),
        State("toast-state", "data"),
        State("toast-notification", "style"),
        prevent_initial_call=True,
    )
    def hide_toast_notification(n_intervals, toast_state, current_style):
        """当计时器触发时隐藏通知"""
        if not toast_state or not toast_state.get("visible"):
            raise PreventUpdate

        # 设置隐藏样式
        hidden_style = dict(current_style)
        hidden_style["transform"] = "translateX(420px)"
        hidden_style["opacity"] = "0"

        # 返回：隐藏样式、禁用计时器、重置计数器为 0、更新状态为不可见
        return hidden_style, True, 0, {"visible": False}
