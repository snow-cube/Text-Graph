from text_graph import TextGraph


def process_shortest_path(
    word1, word2, text_graph, style_state, is_graph_displayed=True
):
    """处理最短路径的通用函数"""
    if isinstance(text_graph, str):
        tg = TextGraph(text_graph or "")
    else:
        tg = text_graph

    if not word1 or not word2 or word1 == word2:
        return [], f"请提供两个不同的单词", style_state

    # 检查单词是否存在于图中
    word1_exists = word1.lower() in tg.nodes
    word2_exists = word2.lower() in tg.nodes

    if not word1_exists and not word2_exists:
        return [], f"单词 '{word1}' 和 '{word2}' 都不存在于图中", style_state
    elif not word1_exists:
        return [], f"单词 '{word1}' 不存在于图中", style_state
    elif not word2_exists:
        return [], f"单词 '{word2}' 不存在于图中", style_state

    # Always calculate the shortest path result
    path, total_weight = (
        tg.get_shortest_path(word1, word2)
        if hasattr(tg, "get_shortest_path")
        else ([], 0)
    )

    # Only update the visual style if the graph is displayed
    if is_graph_displayed:
        style_state["bridge_words"] = []
        style_state["shortest_path"] = path

        # 只有当单词在图中存在时，才添加到选中节点列表
        selected_nodes = []
        if word1 in tg.nodes:
            selected_nodes.append(word1)
        if word2 in tg.nodes:
            selected_nodes.append(word2)
        style_state["selected_nodes"] = selected_nodes

        style_state["highlighted_edges"] = []

        highlighted_edges = []
        if path and len(path) > 1:
            for i in range(len(path) - 1):
                highlighted_edges.append(
                    {"source": path[i], "target": path[i + 1], "type": "shortest"}
                )
        style_state["highlighted_edges"] = highlighted_edges

    if path and len(path) > 1:
        msg = f"最短路径（{word1} → {word2}，权重和: {total_weight}）：" + " → ".join(
            path
        )
    else:
        msg = f"未找到 {word1} → {word2} 的路径"

    return path, msg, style_state
