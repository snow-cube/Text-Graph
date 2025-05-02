from dash import Input, Output, State
from text_graph import TextGraph


def register_pagerank_callback(app):
    @app.callback(
        Output("pagerank-store", "data"),
        [Input("pagerank-toggle", "value"), Input("graph-store", "data")],
        [State("pagerank-store", "data")],
    )
    def calculate_pagerank(toggle_value, graph_text, current_pr_data):
        """计算 PageRank 并存储结果"""
        # 如果未启用 PageRank 计算，返回空数据
        if not toggle_value or "enabled" not in toggle_value:
            return {}

        # 如果没有图数据，返回空数据
        if not graph_text:
            return {}

        # 计算 PageRank
        tg = TextGraph(graph_text)
        pagerank = tg.calculate_pagerank()

        # 构建包含原始值和格式化值的字典
        pr_data = {
            "raw": pagerank,
            "formatted": {node: f"{value:.6f}" for node, value in pagerank.items()},
        }

        return pr_data
