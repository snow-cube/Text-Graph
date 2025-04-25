from callbacks.node_click import register_node_click_callback
from callbacks.bridge_query import register_bridge_query_callback
from callbacks.style import register_style_callback
from callbacks.image import register_image_callback
from callbacks.clear import register_clear_callback
from callbacks.upload import register_upload_callback
from callbacks.mode_switch import register_mode_switch_callback


def register_callbacks(app):
    register_upload_callback(app)
    register_node_click_callback(app)
    register_bridge_query_callback(app)
    register_clear_callback(app)
    register_image_callback(app)
    register_style_callback(app)
    register_mode_switch_callback(app)
