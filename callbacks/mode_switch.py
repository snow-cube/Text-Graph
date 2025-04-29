from dash import Output, Input, State
import dash
from graph_process_utils.bridge_utils import process_bridge_words
from graph_process_utils.shortest_path_utils import process_shortest_path
from message_templates import bridge_result_message, shortest_path_result_message


def register_mode_switch_callback(app):
    @app.callback(
        [
            Output("node-info", "children", allow_duplicate=True),
            Output("style-store", "data", allow_duplicate=True),
        ],
        Input("query-mode-switch", "value"),
        [
            State("graph-store", "data"),
            State("style-store", "data"),
            State("graph-display-state", "data"),  # Add display state
        ],
        prevent_initial_call=True,
    )
    def update_on_mode_switch(mode, graph_text, style_state, display_state):
        # 只根据已选节点进行处理
        selected_nodes = style_state.get("selected_nodes") if style_state else None
        if not selected_nodes or len(selected_nodes) != 2:
            return dash.no_update, dash.no_update

        # Check if graph is displayed
        is_graph_displayed = display_state.get('show', False)

        word1, word2 = selected_nodes
        if word1 and word2 and word1 != word2:
            if mode == "shortest":
                path, msg_text, updated_style = process_shortest_path(
                    word1, word2, graph_text, style_state, is_graph_displayed
                )
                # 使用模板生成结果
                return shortest_path_result_message(msg_text), updated_style
            else:
                bridges, msg_text, updated_style = process_bridge_words(
                    word1, word2, graph_text, style_state, is_graph_displayed
                )
                # 使用模板生成结果
                return bridge_result_message(msg_text), updated_style

        return dash.no_update, dash.no_update
