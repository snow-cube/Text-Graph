from dash import Output, Input
from style_utils import (
    get_base_stylesheet,
    get_selected_node_style,
    get_in_edge_style,
    get_out_edge_style,
    get_bridge_word_style,
    get_shortest_path_node_style,
    get_shortest_path_edge_style,
    get_bridge_edge_style,
)


def register_style_callback(app):
    @app.callback(
        Output("cytoscape", "stylesheet"),
        Input("style-store", "data"),
        prevent_initial_call=True,
    )
    def update_stylesheet(style_state):
        stylesheet = get_base_stylesheet()
        selected_nodes = style_state.get("selected_nodes", [])
        if len(selected_nodes) >= 1:
            node1 = selected_nodes[0]
            stylesheet.append(
                {
                    "selector": f"node[id = '{node1}']",
                    "style": {
                        "background-color": "#26a69a",
                        "border-color": "#00897b",
                        "border-width": 4,
                        "text-outline-color": "#00897b",
                        "shadow-color": "#26a69a",
                        "shadow-blur": 13,
                        "shadow-opacity": 0.6,
                        "font-size": "19px",
                        "color": "#fff",
                        "z-index": 8,
                    },
                }
            )
        if len(selected_nodes) >= 2:
            node2 = selected_nodes[1]
            stylesheet.append(
                {
                    "selector": f"node[id = '{node2}']",
                    "style": {
                        "background-color": "#b2dfdb",
                        "border-color": "#4db6ac",
                        "border-width": 3,
                        "text-outline-color": "#4db6ac",
                        "shadow-color": "#b2dfdb",
                        "shadow-blur": 8,
                        "shadow-opacity": 0.5,
                        "font-size": "18px",
                        "z-index": 2,
                    },
                }
            )
        if len(selected_nodes) > 2:
            for node in selected_nodes[2:]:
                stylesheet.append(get_selected_node_style(node))
        for bridge in style_state.get("bridge_words", []):
            stylesheet.append(get_bridge_word_style(bridge))
        for node in style_state.get("shortest_path", [])[1:-1]:
            stylesheet.append(get_shortest_path_node_style(node))
        for edge in style_state.get("highlighted_edges", []):
            if edge["type"] == "in":
                stylesheet.append(get_in_edge_style(edge["source"], edge["target"]))
            elif edge["type"] == "out":
                stylesheet.append(get_out_edge_style(edge["source"], edge["target"]))
            elif edge["type"] == "bridge":
                stylesheet.append(get_bridge_edge_style(edge["source"], edge["target"]))
            elif edge["type"] == "shortest":
                stylesheet.append(
                    get_shortest_path_edge_style(edge["source"], edge["target"])
                )
        return stylesheet
