# 更新样式以显示随机游走
def update_style_for_walk(style_state, walked_nodes, walked_edges):
    # style_state["selected_nodes"] = []
    # style_state["bridge_words"] = []
    style_state["random_walk_nodes"] = walked_nodes

    # 添加起始节点和当前节点的特殊标记
    if walked_nodes:
        style_state["start_node"] = walked_nodes[0]  # 第一个节点为起始节点
        style_state["current_node"] = walked_nodes[-1]  # 最后一个节点为当前节点

    # 添加高亮边
    highlighted_edges = []
    for src, tgt, _ in walked_edges:
        highlighted_edges.append({"source": src, "target": tgt, "type": "random_walk"})
    style_state["highlighted_edges"] = highlighted_edges

    return style_state
