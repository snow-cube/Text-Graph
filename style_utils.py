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


def get_bridge_word_style(word):
    # 橙黄色高亮桥接词节点，弱于选中节点
    return {
        "selector": f"node[id = '{word}']",
        "style": {
            "background-color": "#ffe082",  # 柔和橙黄
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


def get_shortest_path_node_style(word):
    # 高亮最短路节点（浅明亮紫色系，介于前两次）
    return {
        "selector": f"node[id = '{word}']",
        "style": {
            "background-color": "#e1bee7",  # 浅紫色
            "border-color": "#ba68c8",  # 明亮紫色边框
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
    # 高亮最短路边（浅明亮紫色系，介于前两次）
    return {
        "selector": f"edge[source = '{source}'][target = '{target}']",
        "style": {
            "line-color": "#ba68c8",  # 浅明亮紫色
            "target-arrow-color": "#ba68c8",
            "width": 5,
            "opacity": 1,
            "z-index": 999,
            "line-style": "solid",
            "arrow-scale": 1.5,
            "text-background-opacity": 1,
            "text-background-color": "#ede7f6",  # 淡紫色
            "text-background-shape": "round-rectangle",
            "text-border-width": 1,
            "text-border-color": "#ba68c8",
            "text-border-opacity": 0.8,
            "font-size": "14px",
            "color": "#7b1fa2",  # 明亮紫色字体
            "font-weight": "bold",
        },
    }


def get_bridge_edge_style(source, target):
    # 桥接词边：黄色调
    return {
        "selector": f"edge[source = '{source}'][target = '{target}']",
        "style": {
            "line-color": "#ffb300",  # 明亮黄色
            "target-arrow-color": "#ffb300",
            "width": 5,
            "opacity": 1,
            "z-index": 999,
            "line-style": "solid",
            "arrow-scale": 1.5,
            "text-background-opacity": 1,
            "text-background-color": "#fff8e1",  # 极浅黄
            "text-background-shape": "round-rectangle",
            "text-border-width": 1,
            "text-border-color": "#ffb300",
            "text-border-opacity": 0.8,
            "font-size": "14px",
            "color": "#ff8f00",  # 深黄字体
            "font-weight": "bold",
        },
    }
