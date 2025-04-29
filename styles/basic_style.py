def get_base_stylesheet():
    return [
        {
            "selector": "node",
            "style": {
                "label": "data(label)",
                "background-color": "#1ecbe1",  # 明亮青蓝色
                "color": "#FFFFFF",
                "font-size": "18px",
                "font-weight": "bold",
                "text-valign": "center",
                "text-halign": "center",
                "border-width": 2,
                "border-color": "#008080",  # 更加明显的青色
                "shape": "ellipse",
                "width": "45px",
                "height": "45px",
                "text-outline-width": 2,
                "text-outline-color": "#008080",
                "shadow-blur": 10,
                "shadow-color": "#8ee6e6",
                "shadow-offset-x": 2,
                "shadow-offset-y": 2,
                "shadow-opacity": 0.5,
            },
        },
        {
            "selector": "edge",
            "style": {
                "label": "data(weight)",
                "curve-style": "bezier",
                "target-arrow-shape": "triangle",
                "target-arrow-color": "#666",
                "line-color": "#666",
                "width": "mapData(weight, 1, 10, 2, 6)",
                "font-size": "12px",
                "color": "#555",
            },
        },
    ]


def get_reset_style_state():
    return {
        "selected_nodes": [],
        "bridge_words": [],
        "highlighted_edges": [],
        "base_style_applied": True,
        "shortest_path": [],
        "random_walk_nodes": [],
        "start_node": None,
        "current_node": None,
    }
