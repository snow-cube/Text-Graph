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
        # {
        #     "selector": "node.selected",
        #     "style": {
        #         "background-color": "#FF5733",
        #         "border-color": "#C70039",
        #         "border-width": 4,
        #         "text-outline-color": "#C70039",
        #         "shadow-color": "#FF5733",
        #         "shadow-blur": 15,
        #         "shadow-opacity": 0.8,
        #         "font-size": "20px",
        #     },
        # },
        # {
        #     "selector": "edge.connected",
        #     "style": {
        #         "line-color": "#FF5733",
        #         "target-arrow-color": "#FF5733",
        #         "width": "data(weight)",
        #         "opacity": 1,
        #     },
        # },
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