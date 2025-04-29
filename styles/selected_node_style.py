def get_selected_node_style(word):
    return {
        "selector": f"node[id = '{word}']",
        "style": {
            "background-color": "#cfd8dc",  # 浅蓝灰，和谐不显眼
            "border-color": "#90a4ae",
            "border-width": 2,
            "text-outline-color": "#90a4ae",
            "shadow-color": "#cfd8dc",
            "shadow-blur": 6,
            "shadow-opacity": 0.3,
            "font-size": "17px",
            "color": "#37474f",
            "z-index": 1,
        },
    }


def get_first_selected_node_style(word):
    # 应用于第一个选中节点
    return {
        "selector": f"node[id = '{word}']",
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


def get_second_selected_node_style(word):
    # 应用于第二个选中节点
    return {
        "selector": f"node[id = '{word}']",
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


def get_in_edge_style(source, word):
    return {
        "selector": f"edge[source = '{source}'][target = '{word}']",
        "style": {
            "line-color": "#F39C12",
            "target-arrow-color": "#F39C12",
            "width": 5,
            "opacity": 1,
            "z-index": 999,
            "line-style": "solid",
            "text-background-opacity": 1,
            "text-background-color": "#FEF5E7",
            "text-background-shape": "round-rectangle",
            "text-border-width": 1,
            "text-border-color": "#F39C12",
            "text-border-opacity": 0.8,
            "font-size": "14px",
            "color": "#D35400",
            "font-weight": "bold",
        },
    }


def get_out_edge_style(word, target):
    return {
        "selector": f"edge[source = '{word}'][target = '{target}']",
        "style": {
            "line-color": "#00BCD4",
            "target-arrow-color": "#00BCD4",
            "width": 5,
            "opacity": 1,
            "z-index": 999,
            "line-style": "solid",
            "arrow-scale": 1.5,
            "text-background-opacity": 1,
            "text-background-color": "#E0F7FA",
            "text-background-shape": "round-rectangle",
            "text-border-width": 1,
            "text-border-color": "#00BCD4",
            "text-border-opacity": 0.8,
            "font-size": "14px",
            "color": "#0097A7",
            "font-weight": "bold",
        },
    }
