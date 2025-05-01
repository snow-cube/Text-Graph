"""
UI 状态控制模块
根据UI状态更新按钮样式和禁用状态
"""

from dash import Output, Input
from styles.button_styles import (
    RANDOM_WALK_START_BUTTON_STYLE,
    RANDOM_WALK_STOP_BUTTON_STYLE,
    RANDOM_WALK_STOP_BUTTON_HIDDEN_STYLE,
    get_save_walk_button_style,
    get_query_button_style,
    get_node_query_button_style,
)


def register_ui_controls_callback(app):
    """注册 UI 控制回调"""

    @app.callback(
        [
            # 随机游走按钮控制
            Output("random-walk-btn", "style"),
            Output("stop-walk-btn", "style"),
            # 游走保存按钮控制
            Output("save-walk-btn", "disabled"),
            Output("save-walk-btn", "style"),
            # 查询功能控制
            Output("bridge-word1", "disabled"),
            Output("bridge-word2", "disabled"),
            Output("bridge-shortest-query-btn", "disabled"),
            Output("bridge-shortest-query-btn", "style"),
            Output("node-query-input", "disabled"),
            Output("node-query-btn", "disabled"),
            Output("node-query-btn", "style"),
        ],
        [Input("ui-state-store", "data")],
        prevent_initial_call=True,
    )
    def update_ui_controls(ui_state):
        """
        根据 UI 状态更新 UI 控件

        Args:
            ui_state: UI 状态字典，包含以下键：
                - walk_active: 是否正在随机游走
                - save_enabled: 是否可以保存游走结果
                - query_enabled: 是否启用查询功能

        Returns:
            UI 控件更新元组
        """
        # 从 UI 状态获取值，如果不存在则使用默认值
        walk_active = ui_state.get("walk_active", False)
        save_enabled = ui_state.get("save_enabled", False)
        query_enabled = ui_state.get("query_enabled", True)

        # 随机游走按钮状态
        if walk_active:
            random_walk_btn_style = {"display": "none"}
            stop_walk_btn_style = RANDOM_WALK_STOP_BUTTON_STYLE
        else:
            random_walk_btn_style = RANDOM_WALK_START_BUTTON_STYLE
            stop_walk_btn_style = RANDOM_WALK_STOP_BUTTON_HIDDEN_STYLE

        # 保存按钮状态
        save_btn_disabled = not save_enabled
        save_btn_style = get_save_walk_button_style(enabled=save_enabled)

        # 查询功能状态
        query_disabled = not query_enabled
        query_btn_style = get_query_button_style(enabled=query_enabled)
        node_query_btn_style = get_node_query_button_style(enabled=query_enabled)

        return (
            random_walk_btn_style,
            stop_walk_btn_style,
            save_btn_disabled,
            save_btn_style,
            query_disabled,
            query_disabled,
            query_disabled,
            query_btn_style,
            query_disabled,
            query_disabled,
            node_query_btn_style,
        )
