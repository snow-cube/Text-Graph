from text_graph import TextGraph


def process_bridge_words(word1, word2, text_graph, elements, style_state):
    """处理桥接词的通用函数

    Args:
        word1: 第一个单词
        word2: 第二个单词
        text_graph: TextGraph实例或原始文本
        elements: 图的元素列表
        style_state: 当前样式状态字典

    Returns:
        tuple: (桥接词列表, 信息消息, 更新后的样式状态)
    """
    if isinstance(text_graph, str):
        tg = TextGraph(text_graph or "")
    else:
        tg = text_graph

    if not word1 or not word2 or word1 == word2:
        return [], f"请提供两个不同的单词", style_state

    style_state["shortest_path"] = []
    style_state["bridge_words"] = []
    style_state["highlighted_edges"] = []

    bridges = tg.get_bridge_words(word1, word2)
    style_state["selected_nodes"] = [word1, word2]
    style_state["bridge_words"] = bridges

    highlighted_edges = []
    if bridges and elements and isinstance(elements, list):
        for elem in elements:
            data = elem.get("data", {})
            if "source" in data and "target" in data:
                if data.get("source") == word1 and data.get("target") in bridges:
                    highlighted_edges.append(
                        {
                            "source": word1,
                            "target": data.get("target"),
                            "type": "bridge",
                        }
                    )
                if data.get("source") in bridges and data.get("target") == word2:
                    highlighted_edges.append(
                        {
                            "source": data.get("source"),
                            "target": word2,
                            "type": "bridge",
                        }
                    )
    style_state["highlighted_edges"] = highlighted_edges

    if bridges:
        msg = f"桥接词（{word1} → ? → {word2}）：" + "，".join(bridges)
    else:
        msg = f"未找到 {word1} → ? → {word2} 的桥接词"

    return bridges, msg, style_state
