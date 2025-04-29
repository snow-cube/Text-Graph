from dash import Output, Input, State
import dash
from graph_process_utils.bridge_utils import process_bridge_words
from graph_process_utils.shortest_path_utils import process_shortest_path
from message_templates import bridge_result_message, shortest_path_result_message


def register_bridge_shortest_query_callback(app):
    @app.callback(
        [
            Output("bridge-word1", "value", allow_duplicate=True),
            Output("bridge-word2", "value", allow_duplicate=True),
            Output("node-info", "children", allow_duplicate=True),
            Output("style-store", "data", allow_duplicate=True),
        ],
        [Input("bridge-shortest-query-btn", "n_clicks")],
        [
            State("bridge-word1", "value"),
            State("bridge-word2", "value"),
            State("graph-store", "data"),
            State("style-store", "data"),
            State("query-mode-switch", "value"),
            State("graph-display-state", "data"),
            State("random-walk-store", "data"),
        ],
        prevent_initial_call=True,
    )
    def query_bridge_shortest_from_input(
        n_clicks, word1, word2, graph_text, style_state, mode, display_state, walk_state
    ):
        if not n_clicks:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update

        # 检查是否处于随机游走状态，如果是则忽略查询
        if walk_state and walk_state.get("is_active", False):
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update

        # Check if graph is displayed
        is_graph_displayed = display_state.get("show", False)

        if mode == "shortest":
            path, msg_text, updated_style = process_shortest_path(
                word1, word2, graph_text, style_state, is_graph_displayed
            )
            # 使用模板生成结果
            return word1, word2, shortest_path_result_message(msg_text), updated_style
        else:
            bridges, msg_text, updated_style = process_bridge_words(
                word1, word2, graph_text, style_state, is_graph_displayed
            )
            # 使用模板生成结果
            return word1, word2, bridge_result_message(msg_text), updated_style
