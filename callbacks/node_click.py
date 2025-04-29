from dash import Output, Input, State, html
import dash
from graph_process_utils.bridge_utils import process_bridge_words
from graph_process_utils.shortest_path_utils import process_shortest_path


def register_node_click_callback(app):
    @app.callback(
        [
            Output("node-info", "children", allow_duplicate=True),
            Output("style-store", "data", allow_duplicate=True),
            Output("bridge-word1", "value", allow_duplicate=True),
            Output("bridge-word2", "value", allow_duplicate=True),
            Output("bridge-result", "children", allow_duplicate=True),
        ],
        [Input("cytoscape", "tapNodeData")],
        [
            State("style-store", "data"),
            State("cytoscape", "elements"),
            State("graph-store", "data"),
            State("query-mode-switch", "value"),
        ],
        prevent_initial_call=True,
    )
    def handle_node_click(tap_node_data, style_state, elements, graph_text, mode):
        if not tap_node_data:
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
                path, msg, updated_style = process_shortest_path(
                    w1, w2, graph_text, style_state
                )
                return dash.no_update, updated_style, w1, w2, msg
            else:
                bridges, msg, updated_style = process_bridge_words(
                    w1, w2, graph_text, style_state
                )
                return dash.no_update, updated_style, w1, w2, msg
        style_state["bridge_words"] = []
        style_state["shortest_path"] = []
        style_state["highlighted_edges"] = []
        if len(selected_nodes) == 1:
            word = selected_nodes[0]
            highlighted_edges = []
            in_edges = []
            out_edges = []
            if isinstance(elements, list):
                for elem in elements:
                    data = elem.get("data", {})
                    if "source" in data and "target" in data:
                        if data["target"] == word:
                            in_edges.append((data["source"], data.get("weight", 1)))
                            highlighted_edges.append(
                                {"source": data["source"], "target": word, "type": "in"}
                            )
                        elif data["source"] == word:
                            out_edges.append((data["target"], data.get("weight", 1)))
                            highlighted_edges.append(
                                {
                                    "source": word,
                                    "target": data["target"],
                                    "type": "out",
                                }
                            )
            style_state["highlighted_edges"] = highlighted_edges
            info_components = [
                html.H4(f"单词: {word}", style={"color": "#0077B6"}),
                html.Hr(),
                html.Div(
                    [
                        html.H5("入边 (前驱词):", style={"color": "#444"}),
                        (
                            html.Ul(
                                [
                                    html.Li(f"{source} → {word} (权重: {weight})")
                                    for source, weight in sorted(
                                        in_edges, key=lambda x: -x[1]
                                    )
                                ]
                            )
                            if in_edges
                            else html.P("无入边")
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.H5("出边 (后继词):", style={"color": "#444"}),
                        (
                            html.Ul(
                                [
                                    html.Li(f"{word} → {target} (权重: {weight})")
                                    for target, weight in sorted(
                                        out_edges, key=lambda x: -x[1]
                                    )
                                ]
                            )
                            if out_edges
                            else html.P("无出边")
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.H5("统计:", style={"color": "#444"}),
                        html.P(f"总前驱单词数: {len(in_edges)}"),
                        html.P(f"总后继单词数: {len(out_edges)}"),
                        html.P(f"总关联单词数: {len(in_edges) + len(out_edges)}"),
                    ]
                ),
            ]
            return (
                info_components,
                style_state,
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )
        if len(selected_nodes) == 0:
            return (
                "请点击一个节点查看详细信息或选择两个节点查询桥接词",
                style_state,
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )
        else:
            return (
                "请只选择一个节点查看详情或选择恰好两个节点查询桥接词",
                style_state,
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )
