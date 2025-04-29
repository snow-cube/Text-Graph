from dash import Output, Input, State
import dash
from graph_process_utils.bridge_utils import process_bridge_words
from graph_process_utils.shortest_path_utils import process_shortest_path


def register_bridge_shortest_query_callback(app):
    @app.callback(
        [
            Output("bridge-word1", "value", allow_duplicate=True),
            Output("bridge-word2", "value", allow_duplicate=True),
            Output("bridge-result", "children", allow_duplicate=True),
            Output("style-store", "data", allow_duplicate=True),
        ],
        [Input("bridge-shortest-query-btn", "n_clicks")],
        [
            State("bridge-word1", "value"),
            State("bridge-word2", "value"),
            State("graph-store", "data"),
            State("style-store", "data"),
            State("query-mode-switch", "value"),
            State("graph-display-state", "data"),  # Add display state
        ],
        prevent_initial_call=True,
    )
    def query_bridge_shortest_from_input(
        n_clicks, word1, word2, graph_text, style_state, mode, display_state
    ):
        if not n_clicks:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update

        # Check if graph is displayed
        is_graph_displayed = display_state.get("show", False)

        if mode == "shortest":
            path, msg, updated_style = process_shortest_path(
                word1, word2, graph_text, style_state, is_graph_displayed
            )
            return word1, word2, msg, updated_style
        else:
            bridges, msg, updated_style = process_bridge_words(
                word1, word2, graph_text, style_state, is_graph_displayed
            )
            return word1, word2, msg, updated_style
