from dash import Output, Input, State
from styles.basic_style import get_base_stylesheet

from styles.selected_node_style import (
    get_selected_node_style,
    get_in_edge_style,
    get_out_edge_style,
    get_first_selected_node_style,
    get_second_selected_node_style,
)

from styles.bridge_word_style import get_bridge_word_style, get_bridge_edge_style
from styles.shortest_path_style import (
    get_shortest_path_node_style,
    get_shortest_path_edge_style,
)
from styles.random_walk_style import (
    get_random_walk_node_style,
    get_random_walk_edge_style,
    get_random_walk_start_node_style,
    get_random_walk_current_node_style,
)


def register_style_callback(app):
    @app.callback(
        Output("cytoscape", "stylesheet"),
        Input("style-store", "data"),
        State("graph-display-state", "data"),
        prevent_initial_call=True,
    )
    def update_stylesheet(style_state, display_state):
        # 只在图显示时更新样式
        if not display_state or not display_state.get("show", False):
            return get_base_stylesheet()

        stylesheet = get_base_stylesheet()
        selected_nodes = style_state.get("selected_nodes", [])
        if len(selected_nodes) >= 1:
            stylesheet.append(get_first_selected_node_style(selected_nodes[0]))
        if len(selected_nodes) >= 2:
            stylesheet.append(get_second_selected_node_style(selected_nodes[1]))
        if len(selected_nodes) > 2:
            for node in selected_nodes[2:]:
                stylesheet.append(get_selected_node_style(node))
        for bridge in style_state.get("bridge_words", []):
            stylesheet.append(get_bridge_word_style(bridge))
        for node in style_state.get("shortest_path", [])[1:-1]:
            stylesheet.append(get_shortest_path_node_style(node))

        # 处理随机游走样式
        random_walk_nodes = style_state.get("random_walk_nodes", [])
        start_node = style_state.get("start_node")
        current_node = style_state.get("current_node")

        # 第一种情况：开始节点和当前节点相同
        if start_node and start_node == current_node:
            # 使用起始节点样式，它的优先级更高
            stylesheet.append(get_random_walk_start_node_style(start_node))
        # 第二种情况：开始节点和当前节点不同
        elif start_node and current_node:
            # 起始节点使用特定的起始节点样式
            stylesheet.append(get_random_walk_start_node_style(start_node))
            # 当前节点使用特定的当前节点样式
            stylesheet.append(get_random_walk_current_node_style(current_node))

        # 为其他随机游走节点添加基本样式（排除开始和当前节点）
        if random_walk_nodes:
            for node in random_walk_nodes:
                if node != start_node and node != current_node:
                    stylesheet.append(get_random_walk_node_style(node))

        # Apply edge styles in the correct order
        for edge in style_state.get("highlighted_edges", []):
            if edge.get("type") == "in":
                stylesheet.append(get_in_edge_style(edge["source"], edge["target"]))
            elif edge.get("type") == "out":
                stylesheet.append(get_out_edge_style(edge["source"], edge["target"]))
            elif edge.get("type") == "bridge":
                stylesheet.append(get_bridge_edge_style(edge["source"], edge["target"]))
            elif edge.get("type") == "shortest":
                stylesheet.append(
                    get_shortest_path_edge_style(edge["source"], edge["target"])
                )
            elif edge.get("type") == "random_walk":
                stylesheet.append(
                    get_random_walk_edge_style(edge["source"], edge["target"])
                )

        return stylesheet
