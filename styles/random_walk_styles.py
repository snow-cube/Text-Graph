def get_random_walk_node_style(word):
    return {
        "selector": f"node[id = '{word}']",
        "style": {
            "background-color": "#fee5f0",
            "border-color": "#f06292",
            "border-width": 3,
            "text-outline-color": "#f06292",
            "shadow-color": "#fee5f0",
            "shadow-blur": 8,
            "shadow-opacity": 0.5,
            "font-size": "18px",
            "z-index": 3,
        },
    }


def get_random_walk_start_node_style(word):
    return {
        "selector": f"node[id = '{word}']",
        "style": {
            "background-color": "#ec6a9c",
            "border-color": "#c2185b",
            "border-width": 4,
            "text-outline-color": "#c2185b",
            "shadow-color": "#ec6a9c",
            "shadow-blur": 13,
            "shadow-opacity": 0.6,
            "font-size": "19px",
            "color": "#fff",
            "z-index": 8,
        },
    }


def get_random_walk_current_node_style(word):
    return {
        "selector": f"node[id = '{word}']",
        "style": {
            "background-color": "#f48fb1",
            "border-color": "#ec407a",
            "border-width": 3,
            "text-outline-color": "#ec407a",
            "shadow-color": "#f48fb1",
            "shadow-blur": 10,
            "shadow-opacity": 0.5,
            "font-size": "18px",
            "z-index": 7,
            "shadow-offset-x": 0,
            "shadow-offset-y": 0,
            "shadow-blur": 15,
            "shadow-opacity": 0.8,
            "shadow-color": "#f06292",
        },
    }


def get_random_walk_edge_style(source, target):
    return {
        "selector": f"edge[source = '{source}'][target = '{target}']",
        "style": {
            "line-color": "#ec407a",
            "target-arrow-color": "#ec407a",
            "width": 5,
            "opacity": 1,
            "z-index": 999,
            "line-style": "solid",
            "arrow-scale": 1.5,
            "text-background-opacity": 1,
            "text-background-color": "#fce4ec",
            "text-background-shape": "round-rectangle",
            "text-border-width": 1,
            "text-border-color": "#ec407a",
            "text-border-opacity": 0.8,
            "font-size": "14px",
        },
    }
