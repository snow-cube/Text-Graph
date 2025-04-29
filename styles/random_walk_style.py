def get_random_walk_node_style(word):
    # 高亮随机游走节点（粉色系列）- 颜色更浅
    return {
        "selector": f"node[id = '{word}']",
        "style": {
            "background-color": "#fee5f0",  # 非常浅的粉色
            "border-color": "#f06292",  # 保持原来的边框色
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
    # 随机游走起始节点的特殊样式 - 颜色略浅
    return {
        "selector": f"node[id = '{word}']",
        "style": {
            "background-color": "#ec6a9c",  # 更浅的深粉色
            "border-color": "#c2185b",  # 深粉色边框
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
    # 随机游走当前节点的特殊样式
    return {
        "selector": f"node[id = '{word}']",
        "style": {
            "background-color": "#f48fb1",  # 中浅粉色
            "border-color": "#ec407a",  # 中等粉色边框
            "border-width": 3,
            "text-outline-color": "#ec407a",
            "shadow-color": "#f48fb1",
            "shadow-blur": 10,
            "shadow-opacity": 0.5,
            "font-size": "18px",
            "z-index": 7,
            "shadow-offset-x": 0,
            "shadow-offset-y": 0,
            "shadow-blur": 15,  # 更大的发光效果
            "shadow-opacity": 0.8,
            "shadow-color": "#f06292",  # 亮粉色阴影
        },
    }


def get_random_walk_edge_style(source, target):
    # 高亮随机游走边（粉色系列）
    return {
        "selector": f"edge[source = '{source}'][target = '{target}']",
        "style": {
            "line-color": "#ec407a",  # 中等粉色
            "target-arrow-color": "#ec407a",
            "width": 5,
            "opacity": 1,
            "z-index": 999,
            "line-style": "solid",
            "arrow-scale": 1.5,
            "text-background-opacity": 1,
            "text-background-color": "#fce4ec",  # 极浅粉色
            "text-background-shape": "round-rectangle",
            "text-border-width": 1,
            "text-border-color": "#ec407a",
            "text-border-opacity": 0.8,
            "font-size": "14px",
        },
    }
