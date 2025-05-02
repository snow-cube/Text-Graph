from dash import Output, Input, State
import dash
from graph_process_utils.bridge_utils import process_bridge_words
from graph_process_utils.shortest_path_utils import process_shortest_path
from graph_process_utils.node_info_utils import process_node_info
from layouts.message_templates import (
    welcome_message,
    warning_message,
    bridge_result_message,
    shortest_path_result_message,
)


def register_node_click_callback(app):
    @app.callback(
        [
            Output("node-info", "children", allow_duplicate=True),
            Output("style-store", "data", allow_duplicate=True),
            Output("bridge-word1", "value", allow_duplicate=True),
            Output("bridge-word2", "value", allow_duplicate=True),
            Output("node-query-input", "value", allow_duplicate=True),
        ],
        [Input("cytoscape", "tapNodeData")],
        [
            State("style-store", "data"),
            State("graph-store", "data"),
            State("query-mode-switch", "value"),
            State("random-walk-store", "data"),
            State("pagerank-store", "data"),
        ],
        prevent_initial_call=True,
    )
    def handle_node_click(
        tap_node_data,
        style_state,
        graph_text,
        mode,
        walk_state,
        pagerank_data,
    ):
        if not tap_node_data:
            return (
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )

        # 检查是否处于随机游走状态，如果是则忽略点击
        if walk_state and walk_state.get("is_active", False):
            return (
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )

        clicked_word = tap_node_data["label"]
        selected_nodes = style_state.get("selected_nodes", [])
        if clicked_word in selected_nodes:
            selected_nodes.remove(clicked_word)
        else:
            selected_nodes.append(clicked_word)
        style_state["selected_nodes"] = selected_nodes

        if len(selected_nodes) == 2:
            w1, w2 = selected_nodes
            if mode == "shortest":
                path, msg_text, updated_style = process_shortest_path(
                    w1, w2, graph_text, style_state
                )
                # 使用模板生成结果
                return (
                    shortest_path_result_message(msg_text),
                    updated_style,
                    w1,
                    w2,
                    dash.no_update,
                )
            else:
                bridges, msg_text, updated_style = process_bridge_words(
                    w1, w2, graph_text, style_state
                )
                # 使用模板生成结果
                return (
                    bridge_result_message(msg_text),
                    updated_style,
                    w1,
                    w2,
                    dash.no_update,
                )

        style_state["bridge_words"] = []
        style_state["shortest_path"] = []
        style_state["highlighted_edges"] = []

        if len(selected_nodes) == 1:
            word = selected_nodes[0]
            node_info, updated_style = process_node_info(
                word, style_state, pagerank_data, graph_text
            )
            return (node_info, updated_style, dash.no_update, dash.no_update, word)

        if len(selected_nodes) == 0:
            # 使用欢迎信息模板
            return (
                welcome_message(),
                style_state,
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )
        else:
            # 使用警告信息模板
            return (
                warning_message(),
                style_state,
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )
