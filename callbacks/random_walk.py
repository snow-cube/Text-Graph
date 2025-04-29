from dash import Output, Input, State, html, dcc
import dash
import json
import random
from graph_process_utils.random_walk_utils import update_style_for_walk
from styles.basic_style import get_reset_style_state
from text_graph import TextGraph
from message_templates import random_walk_result_message, welcome_message


def register_random_walk_callback(app):
    @app.callback(
        [
            Output("random-walk-store", "data"),
            Output("random-walk-interval", "disabled", allow_duplicate=True),
            Output("random-walk-container", "style", allow_duplicate=True),
            Output("random-walk-btn", "style", allow_duplicate=True),
            Output("stop-walk-btn", "style", allow_duplicate=True),
            # Add outputs for disabling interaction elements
            Output("bridge-word1", "disabled", allow_duplicate=True),
            Output("bridge-word2", "disabled", allow_duplicate=True),
            Output("bridge-shortest-query-btn", "disabled", allow_duplicate=True),
            Output("bridge-shortest-query-btn", "style", allow_duplicate=True),
            # Add output to reset style-store
            Output("style-store", "data", allow_duplicate=True),
        ],
        [Input("random-walk-btn", "n_clicks")],
        [
            State("graph-store", "data"),
            State("random-walk-store", "data"),
            State("style-store", "data"),  # Add style-store as state
        ],
        prevent_initial_call=True,
    )
    def start_random_walk(n_clicks, graph_text, walk_state, style_state):
        if not n_clicks:
            return (
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )

        if not graph_text:
            return (
                {},
                True,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )

        # 初始化随机游走状态
        tg = TextGraph(graph_text)
        if not tg.nodes:
            return (
                {},
                True,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )

        # 随机选择起始节点
        current_node = random.choice(list(tg.nodes))

        # 创建初始状态
        walk_state = {
            "current_node": current_node,
            "walked_nodes": [current_node],
            "walked_edges": [],
            "visited_edges": [],  # 使用列表而不是集合，因为JSON不支持集合
            "completed": False,
            "stop_reason": None,
            "is_active": True,  # 标记随机游走正在进行
            "edge_count": {
                json.dumps([src, tgt]): weight
                for (src, tgt), weight in tg.edge_count.items()
            },
        }

        # 重置style-store，清除之前的选择和高亮
        # reset_style = {
        #     "selected_nodes": [],
        #     "bridge_words": [],
        #     "highlighted_edges": [],
        #     "base_style_applied": True,
        #     "random_walk_nodes": [current_node]  # 初始化随机游走节点列表，包含起始节点
        # }
        reset_style = get_reset_style_state()
        # reset_style["random_walk_nodes"] = [current_node]  # 初始化随机游走节点列表，包含起始节点
        # reset_style["start_node"] = current_node  # 设置起始节点
        # reset_style["current_node"] = current_node  # 设置当前节点
        update_style_for_walk(reset_style, [current_node], [])  # 更新样式以显示起始节点

        # 激活间隔计时器，开始逐步游走
        interval_disabled = False

        # 显示停止按钮，隐藏开始按钮
        random_walk_btn_style = {"display": "none"}
        stop_walk_btn_style = {
            "display": "block",
            "fontSize": "15px",
            "padding": "7px 18px",
            "backgroundColor": "#e53935",
            "color": "#fff",
            "border": "none",
            "borderRadius": "4px",
            "cursor": "pointer",
            "marginTop": "10px",
            "width": "100%",
        }

        # 显示随机游走容器
        random_walk_container_style = {"display": "block"}

        # 禁用桥接词/最短路查询相关元素
        query_btn_disabled = True
        query_input_disabled = True
        query_btn_style = {
            "fontSize": "15px",
            "padding": "6px 16px",
            "backgroundColor": "#aaaaaa",  # 灰色表示禁用
            "color": "#fff",
            "border": "none",
            "borderRadius": "4px",
            "cursor": "not-allowed",  # 禁用的光标样式
        }

        return (
            walk_state,
            interval_disabled,
            random_walk_container_style,
            random_walk_btn_style,
            stop_walk_btn_style,
            query_input_disabled,
            query_input_disabled,
            query_btn_disabled,
            query_btn_style,
            reset_style,
        )

    @app.callback(
        [
            Output("random-walk-store", "data", allow_duplicate=True),
            Output("random-walk-interval", "disabled"),
            Output("node-info", "children", allow_duplicate=True),
            Output("style-store", "data", allow_duplicate=True),
        ],
        [Input("random-walk-interval", "n_intervals")],
        [
            State("random-walk-store", "data"),
            State("graph-store", "data"),
            State("style-store", "data"),
            State("graph-display-state", "data"),  # Add graph display state
        ],
        prevent_initial_call=True,
    )
    def update_random_walk(
        n_intervals, walk_state, graph_text, style_state, display_state
    ):
        if not walk_state or walk_state.get("completed", True):
            return dash.no_update, True, dash.no_update, dash.no_update

        # 恢复游走状态
        current_node = walk_state["current_node"]
        walked_nodes = walk_state["walked_nodes"]
        walked_edges = walk_state["walked_edges"]
        visited_edges = set(tuple(edge) for edge in walk_state["visited_edges"])
        edge_count = {
            tuple(json.loads(k)): v for k, v in walk_state["edge_count"].items()
        }

        # 使用 TextGraph 静态方法计算下一步
        next_node, edge_weight = TextGraph.calculate_next_random_walk_step(
            current_node, edge_count
        )

        # 如果没有出边，结束游走
        if next_node is None:
            walk_state["completed"] = True
            walk_state["stop_reason"] = f"节点 '{current_node}' 没有出边"

            # 格式化结果
            result = random_walk_result_message(
                walked_nodes, walked_edges, walk_state["stop_reason"]
            )

            # 仅在图形显示时更新样式
            updated_style = (
                update_style_for_walk(style_state, walked_nodes, walked_edges)
                if display_state.get("show", False)
                else dash.no_update
            )

            return walk_state, True, result, updated_style

        # 检查边是否已访问
        edge = (current_node, next_node)
        if edge in visited_edges:
            # 记录最后一步并结束
            walked_edges.append((current_node, next_node, edge_weight))
            walked_nodes.append(next_node)
            walk_state["completed"] = True
            walk_state["stop_reason"] = f"遇到重复边: {current_node} → {next_node}"

            # 格式化结果
            result = random_walk_result_message(
                walked_nodes, walked_edges, walk_state["stop_reason"]
            )

            # 仅在图形显示时更新样式
            updated_style = (
                update_style_for_walk(style_state, walked_nodes, walked_edges)
                if display_state.get("show", False)
                else dash.no_update
            )

            return walk_state, True, result, updated_style

        # 记录边和节点
        visited_edges.add(edge)
        walked_edges.append((current_node, next_node, edge_weight))
        walked_nodes.append(next_node)

        # 更新状态
        walk_state["current_node"] = next_node
        walk_state["walked_nodes"] = walked_nodes
        walk_state["walked_edges"] = walked_edges
        walk_state["visited_edges"] = [list(edge) for edge in visited_edges]

        # 临时显示当前状态，使用模板
        result = random_walk_result_message(
            walked_nodes, walked_edges, "正在随机游走中..."
        )

        # 仅在图形显示时更新样式
        updated_style = (
            update_style_for_walk(style_state, walked_nodes, walked_edges)
            if display_state.get("show", False)
            else dash.no_update
        )

        return walk_state, False, result, updated_style

    @app.callback(
        [
            Output("random-walk-interval", "disabled", allow_duplicate=True),
            Output("random-walk-container", "style"),
            Output("random-walk-btn", "style"),
            Output("stop-walk-btn", "style"),
            Output("style-store", "data", allow_duplicate=True),
            Output("node-info", "children", allow_duplicate=True),
            # Add outputs for enabling interaction elements again
            Output("bridge-word1", "disabled"),
            Output("bridge-word2", "disabled"),
            Output("bridge-shortest-query-btn", "disabled"),
            Output("bridge-shortest-query-btn", "style"),
            Output("random-walk-store", "data", allow_duplicate=True),
        ],
        [Input("stop-walk-btn", "n_clicks")],
        [
            State("style-store", "data"),
            State("random-walk-store", "data"),
        ],
        prevent_initial_call=True,
    )
    def stop_random_walk(n_clicks, style_state, walk_state):
        if not n_clicks:
            return (
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )

        # 停用间隔计时器
        interval_disabled = True

        # 重置样式状态
        # if "random_walk_nodes" in style_state:
        #     style_state.pop("random_walk_nodes")
        # style_state["highlighted_edges"] = []
        # style_state["start_node"] = None
        # style_state["current_node"] = None
        style_state = get_reset_style_state()

        # 隐藏停止按钮，显示开始按钮
        random_walk_container_style = {"display": "block"}
        random_walk_btn_style = {
            "display": "block",
            "fontSize": "15px",
            "padding": "7px 18px",
            "backgroundColor": "#9c27b0",
            "color": "#fff",
            "border": "none",
            "borderRadius": "4px",
            "cursor": "pointer",
            "marginTop": "10px",
            "width": "100%",
        }
        stop_walk_btn_style = {"display": "none"}

        # 重新启用桥接词/最短路查询相关元素
        query_btn_disabled = False
        query_input_disabled = False
        query_btn_style = {
            "fontSize": "15px",
            "padding": "6px 16px",
            "backgroundColor": "#43a047",
            "color": "#fff",
            "border": "none",
            "borderRadius": "4px",
            "cursor": "pointer",
        }

        # 更新随机游走状态为非活动
        if walk_state:
            walk_state["is_active"] = False
            walk_state["completed"] = True

        return (
            interval_disabled,
            random_walk_container_style,
            random_walk_btn_style,
            stop_walk_btn_style,
            style_state,
            welcome_message(),  # 使用欢迎信息模板
            query_input_disabled,
            query_input_disabled,
            query_btn_disabled,
            query_btn_style,
            walk_state,
        )
