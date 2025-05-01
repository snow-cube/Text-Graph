"""
按钮样式定义模块
提供各种按钮状态的统一样式
"""

# 随机游走开始按钮样式
RANDOM_WALK_START_BUTTON_STYLE = {
    "display": "block",
    "fontSize": "15px",
    "padding": "7px 10px",
    "backgroundColor": "#9c27b0",
    "color": "#fff",
    "border": "none",
    "borderRadius": "4px",
    "cursor": "pointer",
    "flex": "1",
}

# 随机游走停止按钮样式
RANDOM_WALK_STOP_BUTTON_STYLE = {
    "display": "block",
    "fontSize": "15px",
    "padding": "7px 10px",
    "backgroundColor": "#e53935",
    "color": "#fff",
    "border": "none",
    "borderRadius": "4px",
    "cursor": "pointer",
    "flex": "1",
}

# 随机游走停止按钮隐藏样式
RANDOM_WALK_STOP_BUTTON_HIDDEN_STYLE = {"display": "none"}


def get_save_walk_button_style(enabled=False):
    """
    获取随机游走保存按钮样式

    Args:
        enabled: 按钮是否启用

    Returns:
        样式字典
    """
    return {
        "fontSize": "15px",
        "padding": "7px 10px",
        "backgroundColor": "#ff9800" if enabled else "#aaaaaa",
        "color": "#fff",
        "border": "none",
        "borderRadius": "4px",
        "cursor": "pointer" if enabled else "not-allowed",
        "flex": "1",
        "marginLeft": "10px",
    }


def get_query_button_style(enabled=True):
    """
    获取桥接词/最短路查询按钮样式

    Args:
        enabled: 按钮是否启用

    Returns:
        样式字典
    """
    return {
        "fontSize": "15px",
        "padding": "6px 16px",
        "backgroundColor": "#43a047" if enabled else "#aaaaaa",
        "color": "#fff",
        "border": "none",
        "borderRadius": "4px",
        "cursor": "pointer" if enabled else "not-allowed",
    }


def get_node_query_button_style(enabled=True):
    """
    获取节点查询按钮样式

    Args:
        enabled: 按钮是否启用

    Returns:
        样式字典
    """
    return {
        "fontSize": "15px",
        "padding": "6px 16px",
        "backgroundColor": "#2196F3" if enabled else "#aaaaaa",
        "color": "#fff",
        "border": "none",
        "borderRadius": "4px",
        "cursor": "pointer" if enabled else "not-allowed",
    }
