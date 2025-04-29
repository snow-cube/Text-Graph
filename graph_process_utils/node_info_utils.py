from message_templates import node_info_message
from text_graph import TextGraph


def process_node_info(node_name, style_state, pagerank_data, graph_text, is_graph_displayed=True):
    """
    处理节点信息的通用函数，用于获取节点的边信息并更新样式状态

    Args:
        node_name: 节点名称
        style_state: 当前样式状态
        pagerank_data: PageRank数据（如果有）
        graph_text: 图的文本数据
        is_graph_displayed: 是否显示图形（若为False则不更新style_state）

    Returns:
        tuple: (node_info_component, updated_style_state)
            - node_info_component: 包含节点信息的Dash组件
            - updated_style_state: 更新后的样式状态
    """
    # 收集节点的入边和出边
    highlighted_edges = []
    in_edges = []
    out_edges = []

    # 创建TextGraph对象获取边信息
    graph = TextGraph(graph_text)

    # 获取入边
    for source_node, weight in graph.get_in_edges(node_name).items():
        in_edges.append((source_node, weight))
        highlighted_edges.append(
            {"source": source_node, "target": node_name, "type": "in"}
        )

    # 获取出边
    for target_node, weight in graph.get_out_edges(node_name).items():
        out_edges.append((target_node, weight))
        highlighted_edges.append(
            {"source": node_name, "target": target_node, "type": "out"}
        )

    # 只有当图被显示时才更新style_state
    if is_graph_displayed:
        # 重置样式中的查询相关状态
        style_state["bridge_words"] = []
        style_state["shortest_path"] = []
        # 更新高亮边
        style_state["highlighted_edges"] = highlighted_edges

    # 获取PageRank数据（如果有）
    pr_formatted = None
    if pagerank_data and "formatted" in pagerank_data:
        pr_formatted = pagerank_data["formatted"]

    # 使用模板生成节点信息
    node_info = node_info_message(node_name, in_edges, out_edges, pr_formatted)

    return node_info, style_state
