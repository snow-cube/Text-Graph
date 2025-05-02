from dash import Output, Input, State
import dash
from layouts.message_templates import warning_message
from text_graph import TextGraph
from graph_process_utils.node_info_utils import process_node_info


def register_node_query_callback(app):
    @app.callback(
        [
            Output("node-info", "children", allow_duplicate=True),
            Output("style-store", "data", allow_duplicate=True),
            Output("node-query-input", "value"),
        ],
        [Input("node-query-btn", "n_clicks")],
        [
            State("node-query-input", "value"),
            State("style-store", "data"),
            State("graph-store", "data"),
            State("random-walk-store", "data"),
            State("pagerank-store", "data"),
            State("graph-display-state", "data"),
        ],
        prevent_initial_call=True,
    )
    def query_node_from_input(
        n_clicks,
        node_name,
        style_state,
        graph_text,
        walk_state,
        pagerank_data,
        display_state,
    ):
        if not n_clicks or not node_name:
            return dash.no_update, dash.no_update, dash.no_update

        # 检查是否处于随机游走状态，如果是则忽略查询
        if walk_state and walk_state.get("is_active", False):
            return dash.no_update, dash.no_update, dash.no_update

        # 检查节点是否存在
        graph = TextGraph(graph_text)
        if node_name not in graph.nodes:
            return (
                warning_message(f"节点 '{node_name}' 不存在"),
                style_state,
                node_name,
            )  # 保留输入框内容

        # 更新选中节点状态
        style_state["selected_nodes"] = [node_name]

        # 检查图是否显示
        is_graph_displayed = display_state.get("show", False)

        node_info, updated_style = process_node_info(
            node_name, style_state, pagerank_data, graph_text, is_graph_displayed
        )

        # 返回结果并保留输入框内容
        return node_info, updated_style, node_name
