from dash import Output, Input, State
import dash
import json
import random
import datetime
from graph_process_utils.random_walk_utils import (
    update_style_for_walk,
    stop_random_walk_helper,
)
from styles.basic_style import get_reset_style_state
from text_graph import TextGraph
from message_templates import random_walk_result_message


def register_random_walk_callback(app):
    @app.callback(
        [
            Output("random-walk-store", "data"),
            Output("random-walk-interval", "disabled", allow_duplicate=True),
            Output("random-walk-container", "style", allow_duplicate=True),
            Output("style-store", "data", allow_duplicate=True),
            Output("ui-state-store", "data"),
        ],
        [Input("random-walk-btn", "n_clicks")],
        [
            State("graph-store", "data"),
            State("random-walk-store", "data"),
            State("style-store", "data"),
            State("ui-state-store", "data"),
        ],
        prevent_initial_call=True,
    )
    def start_random_walk(n_clicks, graph_text, walk_state, style_state, ui_state):
        if not n_clicks:
            return (
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )

        if not graph_text:
            return {}, True, dash.no_update, dash.no_update, dash.no_update

        # 初始化随机游走状态
        tg = TextGraph(graph_text)
        if not tg.nodes:
            return {}, True, dash.no_update, dash.no_update, dash.no_update

        # 随机选择起始节点
        current_node = random.choice(list(tg.nodes))

        # 创建初始状态
        walk_state = {
            "current_node": current_node,
            "walked_nodes": [current_node],
            "walked_edges": [],
            "visited_edges": [],  # 使用列表而不是集合，因为 JSON 不支持集合
            "completed": False,
            "stop_reason": None,
            "is_active": True,  # 标记随机游走正在进行
            "edge_count": {
                json.dumps([src, tgt]): weight
                for (src, tgt), weight in tg.edge_count.items()
            },
        }

        # 重置 style-store
        reset_style = get_reset_style_state()
        update_style_for_walk(reset_style, [current_node], [])  # 更新样式以显示起始节点

        # 激活间隔计时器，开始逐步游走
        interval_disabled = False

        # 显示随机游走容器
        random_walk_container_style = {"display": "block"}

        # 更新 UI 状态 - 进入游走状态
        updated_ui_state = ui_state.copy() if ui_state else {}
        updated_ui_state.update(
            {
                "walk_active": True,
                "save_enabled": False,
                "query_enabled": False,
            }
        )

        return (
            walk_state,
            interval_disabled,
            random_walk_container_style,
            reset_style,
            updated_ui_state,
        )

    @app.callback(
        [
            Output("random-walk-store", "data", allow_duplicate=True),
            Output("random-walk-interval", "disabled"),
            Output("node-info", "children", allow_duplicate=True),
            Output("style-store", "data", allow_duplicate=True),
            Output("ui-state-store", "data", allow_duplicate=True),
        ],
        [Input("random-walk-interval", "n_intervals")],
        [
            State("random-walk-store", "data"),
            State("graph-store", "data"),
            State("style-store", "data"),
            State("graph-display-state", "data"),
            State("ui-state-store", "data"),
        ],
        prevent_initial_call=True,
    )
    def update_random_walk(
        n_intervals, walk_state, graph_text, style_state, display_state, ui_state
    ):
        if not walk_state or walk_state.get("completed", True):
            return dash.no_update, True, dash.no_update, dash.no_update, dash.no_update

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

        # 更新 UI 状态 - 激活状态下可以保存游走结果
        updated_ui_state = ui_state.copy() if ui_state else {}
        updated_ui_state.update(
            {
                "walk_active": True,
                "save_enabled": True,
                "query_enabled": False,
            }
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

            return (
                walk_state,
                True,  # 停止间隔计时器
                result,
                updated_style,
                updated_ui_state,
            )

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

            return (
                walk_state,
                True,  # 停止间隔计时器
                result,
                updated_style,
                updated_ui_state,
            )

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

        return (
            walk_state,
            False,  # 继续间隔计时器
            result,
            updated_style,
            updated_ui_state,
        )

    @app.callback(
        [
            Output("random-walk-interval", "disabled", allow_duplicate=True),
            Output("random-walk-container", "style", allow_duplicate=True),
            Output("style-store", "data", allow_duplicate=True),
            Output("node-info", "children", allow_duplicate=True),
            Output("random-walk-store", "data", allow_duplicate=True),
            Output("ui-state-store", "data", allow_duplicate=True),
        ],
        [Input("stop-walk-btn", "n_clicks")],
        [
            State("random-walk-store", "data"),
            State("ui-state-store", "data"),
        ],
        prevent_initial_call=True,
    )
    def stop_random_walk(n_clicks, walk_state, ui_state):
        if not n_clicks:
            return (
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )

        # 使用辅助函数处理停止逻辑，自动根据游走节点数量决定是否启用保存按钮
        return stop_random_walk_helper(walk_state, ui_state)

    @app.callback(
        [
            Output("random-walk-interval", "disabled", allow_duplicate=True),
            Output("random-walk-container", "style", allow_duplicate=True),
            Output("style-store", "data", allow_duplicate=True),
            Output("node-info", "children", allow_duplicate=True),
            Output("random-walk-store", "data", allow_duplicate=True),
            Output("ui-state-store", "data", allow_duplicate=True),
        ],
        [Input("graph-store", "data")],  # Trigger when graph data changes
        [
            State("random-walk-store", "data"),
            State("ui-state-store", "data"),
        ],
        prevent_initial_call=True,
    )
    def stop_walk_on_graph_change(graph_data, walk_state, ui_state):
        # Don't stop if no walk is active
        if not walk_state or not walk_state.get("is_active", False):
            return (
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )

        # 使用辅助函数处理停止逻辑，设置特定的停止原因并禁用保存按钮
        return stop_random_walk_helper(
            walk_state,
            ui_state,
            stop_reason="图数据已更改，随机游走自动停止",
            save_enabled=False,
        )

    # 添加保存随机游走结果的回调
    @app.callback(
        Output("download-walk-sequence", "data"),
        [Input("save-walk-btn", "n_clicks")],
        [State("random-walk-store", "data")],
        prevent_initial_call=True,
    )
    def save_walk_sequence(n_clicks, walk_state):
        if not n_clicks or not walk_state or "walked_nodes" not in walk_state:
            return dash.no_update

        # 获取游走节点序列
        walked_nodes = walk_state.get("walked_nodes", [])

        # 生成文件内容 - 只包含单词序列，每行一个单词
        content = " ".join(walked_nodes)

        # 生成下载数据
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"随机游走序列_{timestamp}.txt"

        return dict(
            content=content,
            filename=filename,
            type="text/plain",
        )
