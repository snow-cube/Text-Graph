"""
按钮样式定义模块
提供各种按钮状态的统一样式
"""

# 按钮颜色映射
DEFAULT_BUTTON_COLOR = "#13C4A3"  # 默认按钮颜色
BUTTON_COLORS = {
    "random_walk_start": DEFAULT_BUTTON_COLOR,
    "random_walk_stop": "#f15d58",
    "save_walk": DEFAULT_BUTTON_COLOR,
    "query": DEFAULT_BUTTON_COLOR,
    "node_query": DEFAULT_BUTTON_COLOR,
    "bridge_text": DEFAULT_BUTTON_COLOR,
}


# 通用按钮样式生成函数
def get_button_style(
    button_type,
    enabled=True,
    margin_left=None,
    width=None,
    min_width=None,
    display="block",
    flex=None,
):
    """
    获取统一的按钮样式

    Args:
        button_type: 按钮类型，可选值:
                     'random_walk_start', 'random_walk_stop', 'save_walk',
                     'query', 'node_query', 'bridge_text'
        enabled: 按钮是否启用
        margin_left: 左侧边距
        width: 固定宽度
        min_width: 最小宽度
        display: 显示方式
        flex: flex 布局值

    Returns:
        样式字典
    """
    # 基础样式
    style = {
        "fontSize": "14px",
        "padding": "4px 10px",
        "backgroundColor": (
            BUTTON_COLORS.get(button_type, "#aaaaaa") if enabled else "#aaaaaa"
        ),
        "color": "#fff",
        "border": "none",
        "borderRadius": "6px",
        "cursor": "pointer" if enabled else "not-allowed",
        "display": display,
        "height": "40px",
        "lineHeight": "32px",  # 文本垂直居中
    }

    # 添加可选属性
    if margin_left:
        style["marginLeft"] = margin_left

    if width:
        style["width"] = width

    if min_width:
        style["minWidth"] = min_width

    if flex:
        style["flex"] = flex

    if button_type == "bridge_text":
        style["whiteSpace"] = "nowrap"

    return style


# 随机游走开始按钮样式
RANDOM_WALK_START_BUTTON_STYLE = get_button_style("random_walk_start", flex="1")

# 随机游走停止按钮样式
RANDOM_WALK_STOP_BUTTON_STYLE = get_button_style("random_walk_stop", flex="1")

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
    return get_button_style("save_walk", enabled=enabled, flex="1")


def get_query_button_style(enabled=True):
    """
    获取桥接词/最短路查询按钮样式

    Args:
        enabled: 按钮是否启用

    Returns:
        样式字典
    """
    return get_button_style("query", enabled=enabled, min_width="80px")


def get_node_query_button_style(enabled=True):
    """
    获取节点查询按钮样式

    Args:
        enabled: 按钮是否启用

    Returns:
        样式字典
    """
    return get_button_style("node_query", enabled=enabled, min_width="80px")


def get_bridge_text_button_style(enabled=True):
    """
    获取文本桥接生成按钮样式

    Args:
        enabled: 按钮是否启用

    Returns:
        样式字典
    """
    return get_button_style("bridge_text", enabled=enabled, min_width="80px")


def get_input_style(width="40%", margin_right="0px"):
    """
    获取输入框统一样式

    Args:
        width: 输入框宽度
        margin_right: 右侧间距

    Returns:
        样式字典
    """
    return {
        "width": width,
        "marginRight": margin_right,
        "height": "32px",
        "padding": "4px 8px",
        "fontSize": "14px",
        "borderRadius": "6px",
        "border": "1px solid #ccc",
    }


def get_textarea_style(height="32px", margin_right="0px"):
    """
    获取文本域统一样式

    Args:
        height: 文本域高度
        margin_right: 右侧间距

    Returns:
        样式字典
    """
    return {
        "width": "100%",
        "height": height,
        "padding": "4px 8px",
        "borderRadius": "6px",
        "border": "1px solid #ccc",
        "fontSize": "13px",
        "resize": "none",
        "lineHeight": "18px",
        "verticalAlign": "middle",
        "marginRight": margin_right,
    }
