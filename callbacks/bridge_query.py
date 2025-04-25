from dash import Output, Input, State
import dash
from graph_process_utils.bridge_utils import process_bridge_words
from graph_process_utils.shortest_path_utils import process_shortest_path


def register_bridge_query_callback(app):
    @app.callback(
        [
            Output("bridge-word1", "value", allow_duplicate=True),
            Output("bridge-word2", "value", allow_duplicate=True),
            Output("bridge-result", "children", allow_duplicate=True),
            Output("style-store", "data", allow_duplicate=True),
        ],
        [Input("bridge-query-btn", "n_clicks")],
        [
            State("bridge-word1", "value"),
            State("bridge-word2", "value"),
            State("graph-store", "data"),
            State("style-store", "data"),
            State("cytoscape", "elements"),
            State("query-mode-switch", "value"),
        ],
        prevent_initial_call=True,
    )
    def query_bridge_words_from_input(
        n_clicks, word1, word2, graph_text, style_state, elements, mode
    ):
        if not n_clicks:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update
        if mode == "shortest":
            path, msg, updated_style = process_shortest_path(
                word1, word2, graph_text, elements, style_state
            )
            return word1, word2, msg, updated_style
        else:
            bridges, msg, updated_style = process_bridge_words(
                word1, word2, graph_text, elements, style_state
            )
            return word1, word2, msg, updated_style
