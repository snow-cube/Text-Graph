from styles.basic_styles import get_reset_style_state
from layouts.message_templates import welcome_message


# 更新样式以显示随机游走
def update_style_for_walk(style_state, walked_nodes, walked_edges):
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


# 辅助函数：处理停止随机游走的公共逻辑 - 更新为支持 UI 状态管理
def stop_random_walk_helper(
    walk_state, ui_state=None, stop_reason=None, save_enabled=None
):
    """
    处理停止随机游走的公共逻辑 - 适配 UI 状态管理模式

    Args:
        walk_state: 当前游走状态
        ui_state: 当前 UI 状态，None 则创建新状态
        stop_reason: 停止原因，如果提供则更新到游走状态
        save_enabled: 是否启用保存按钮，None 时自动根据游走节点数量决定

    Returns:
        适用于新回调函数的元组 (interval_disabled, style_state, message, walk_state, ui_state)
    """
    # 停用间隔计时器
    interval_disabled = True

    # 重置样式状态
    reset_style = get_reset_style_state()

    # 更新游走状态
    if walk_state:
        walk_state["is_active"] = False
        walk_state["completed"] = True
        if stop_reason:
            walk_state["stop_reason"] = stop_reason

    # 更新 UI 状态
    updated_ui_state = ui_state.copy() if ui_state else {}

    # 保存按钮启用状态
    if save_enabled is None:
        # 根据游走节点数量决定是否启用保存按钮
        save_enabled = len(walk_state.get("walked_nodes", [])) > 1

    # 更新 UI 状态字典
    updated_ui_state.update(
        {
            "walk_active": False,
            "save_enabled": save_enabled,
            "query_enabled": True,
        }
    )

    return (
        interval_disabled,
        reset_style,
        welcome_message(),  # 重置为欢迎信息
        walk_state,
        updated_ui_state,
    )
