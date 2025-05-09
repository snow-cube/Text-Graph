def get_pagerank_node_style(node_id, pagerank_value):
    """
    为节点添加显示 PageRank 值的样式，由于 label 值更加复杂，为了显示清晰固定了更小的字号等样式，不应被选中样式、随机游走样式等覆盖。

    Args:
        node_id: 节点 ID
        pagerank_value: 该节点的 PageRank 值
    """
    return {
        "selector": f"node[id = '{node_id}']",
        "style": {
            "label": f"{node_id}\n(PR: {pagerank_value})",
            "text-wrap": "wrap",
            "text-max-width": "80px",
            "text-valign": "center",
            "text-background-color": "#f8f9fa",
            "text-background-opacity": 0.6,
            "text-background-padding": "3px",
            "text-background-shape": "round-rectangle",
            "text-border-opacity": 0.5,
            "text-border-width": 1,
            "text-border-color": "#dee2e6",
            "text-halign": "center",
            "font-style": "normal",
            "font-size": "11px",  # 减小字号
            "text-justification": "center",
        },
    }
