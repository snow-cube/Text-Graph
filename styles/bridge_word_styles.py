def get_bridge_word_style(word):
    return {
        "selector": f"node[id = '{word}']",
        "style": {
            "background-color": "#ffe082",
            "border-color": "#ffb300",
            "border-width": 3,
            "text-outline-color": "#ffb300",
            "shadow-color": "#ffe082",
            "shadow-blur": 8,
            "shadow-opacity": 0.5,
            "font-size": "18px",
            "z-index": 2,
        },
    }


def get_bridge_edge_style(source, target):
    return {
        "selector": f"edge[source = '{source}'][target = '{target}']",
        "style": {
            "line-color": "#ffb300",
            "target-arrow-color": "#ffb300",
            "width": 5,
            "opacity": 1,
            "z-index": 999,
            "line-style": "solid",
            "arrow-scale": 1.5,
            "text-background-opacity": 1,
            "text-background-color": "#fff8e1",
            "text-background-shape": "round-rectangle",
            "text-border-width": 1,
            "text-border-color": "#ffb300",
            "text-border-opacity": 0.8,
            "font-size": "14px",
            "color": "#ff8f00",
            "font-weight": "bold",
        },
    }
