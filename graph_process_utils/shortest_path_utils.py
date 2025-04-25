from text_graph import TextGraph


def process_shortest_path(word1, word2, text_graph, elements, style_state):
    """处理最短路径的通用函数"""
    if isinstance(text_graph, str):
        tg = TextGraph(text_graph or "")
    else:
        tg = text_graph

    if not word1 or not word2 or word1 == word2:
        return [], f"请提供两个不同的单词", style_state

    style_state["bridge_words"] = []
    style_state["shortest_path"] = []
    style_state["highlighted_edges"] = []

    path, total_weight = (
        tg.get_shortest_path(word1, word2)
        if hasattr(tg, "get_shortest_path")
        else ([], 0)
    )
    style_state["selected_nodes"] = [word1, word2]
    style_state["shortest_path"] = path

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
