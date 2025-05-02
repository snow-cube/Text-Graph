from callbacks.node_click import register_node_click_callback
from callbacks.bridge_shortest_query import register_bridge_shortest_query_callback
from callbacks.style import register_style_callback
from callbacks.save_image import register_image_callback
from callbacks.clear import register_clear_callback
from callbacks.upload import register_upload_callback
from callbacks.mode_switch import register_mode_switch_callback
from callbacks.random_walk import register_random_walk_callback
from callbacks.graph_display_toggle import register_graph_display_toggle_callback
from callbacks.page_rank import register_pagerank_callback
from callbacks.node_query import register_node_query_callback
from callbacks.bridge_text_generator import register_bridge_text_generator_callback
from callbacks.ui_controls import register_ui_controls_callback
from callbacks.toast_notification import register_toast_callback


def register_callbacks(app):
    """Register all callbacks for the application."""
    register_graph_display_toggle_callback(app)
    register_upload_callback(app)
    register_node_click_callback(app)
    register_bridge_shortest_query_callback(app)
    register_node_query_callback(app)
    register_clear_callback(app)
    register_image_callback(app)
    register_style_callback(app)
    register_mode_switch_callback(app)
    register_random_walk_callback(app)
    register_pagerank_callback(app)
    register_bridge_text_generator_callback(app)
    register_ui_controls_callback(app)
    register_toast_callback(app)
