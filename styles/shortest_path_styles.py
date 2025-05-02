def get_shortest_path_node_style(word):
    # 高亮最短路节点
    return {
        "selector": f"node[id = '{word}']",
        "style": {
            "background-color": "#e1bee7",
            "border-color": "#ba68c8",
            "border-width": 3,
            "text-outline-color": "#ba68c8",
            "shadow-color": "#e1bee7",
            "shadow-blur": 8,
            "shadow-opacity": 0.5,
            "font-size": "18px",
            "z-index": 3,
        },
    }


def get_shortest_path_edge_style(source, target):
    # 高亮最短路边
    return {
        "selector": f"edge[source = '{source}'][target = '{target}']",
        "style": {
            "line-color": "#ba68c8",
            "target-arrow-color": "#ba68c8",
            "width": 5,
            "opacity": 1,
            "z-index": 999,
            "line-style": "solid",
            "arrow-scale": 1.5,
            "text-background-opacity": 1,
            "text-background-color": "#ede7f6",
            "text-background-shape": "round-rectangle",
            "text-border-width": 1,
            "text-border-color": "#ba68c8",
            "text-border-opacity": 0.8,
            "font-size": "14px",
            "color": "#7b1fa2",
            "font-weight": "bold",
        },
    }
