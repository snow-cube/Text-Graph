from text_graph import TextGraph


def process_shortest_path(
    word1, word2, text_graph, style_state, is_graph_displayed=True
):
    """处理最短路径的通用函数"""
    if isinstance(text_graph, str):
        tg = TextGraph(text_graph or "")
    else:
        tg = text_graph

    if not word1:
        return [], f"请提供第一个单词", style_state
    word1 = word1.lower()

    # 检查单词是否存在于图中
    word1_exists = word1 in tg.nodes

    # 处理只有 word1 的情况 - 查询该节点到所有节点的最短路
    if word1 and not word2:
        if not word1_exists:
            return [], f"单词 '{word1}' 不存在于图中", style_state

        all_paths_dict = tg.get_all_shortest_paths(word1)

        # 按路径长度排序
        sorted_paths = sorted(all_paths_dict.items(), key=lambda x: x[1][1])

        # 生成消息
        if sorted_paths:
            msg = f"从 '{word1}' 到所有节点的最短路径:\n\n"
            for target, (path, weight) in sorted_paths[:15]:  # 只显示前 15 个结果
                msg += f"到 '{target}' (权重: {weight}): {' → '.join(path)}\n"

            if len(sorted_paths) > 15:
                msg += f"\n...还有 {len(sorted_paths) - 15} 条路径未显示"
        else:
            msg = f"从 '{word1}' 无法到达任何其他节点"

        # 如果图形被显示，更新样式状态，将该节点标记为选中
        if is_graph_displayed:
            style_state["bridge_words"] = []
            style_state["shortest_path"] = []
            style_state["highlighted_edges"] = []
            style_state["selected_nodes"] = [word1]

        return [], msg, style_state

    word2 = word2.lower()
    if word1 == word2:
        return [], f"请提供两个不同的单词", style_state

    word2_exists = word2 in tg.nodes

    if not word1_exists and not word2_exists:
        return [], f"单词 '{word1}' 和 '{word2}' 都不存在于图中", style_state
    elif not word1_exists:
        return [], f"单词 '{word1}' 不存在于图中", style_state
    elif not word2_exists:
        return [], f"单词 '{word2}' 不存在于图中", style_state

    path, total_weight = tg.get_shortest_path(word1, word2)

    # Only update the visual style if the graph is displayed
    if is_graph_displayed:
        style_state["bridge_words"] = []
        style_state["shortest_path"] = path
        selected_nodes = []
        selected_nodes.append(word1)
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
        msg = f"最短路径 ({word1} → {word2}，权重和: {total_weight}): " + " → ".join(
            path
        )
    else:
        msg = f"未找到 {word1} → {word2} 的路径"

    return path, msg, style_state
