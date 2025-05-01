from dash import Output, Input, State, html
import dash
from text_graph import TextGraph
from message_templates import bridge_text_result_message

def register_bridge_text_generator_callback(app):
    @app.callback(
        Output("node-info", "children", allow_duplicate=True),
        [Input("generate-bridge-text-btn", "n_clicks")],
        [
            State("bridge-text-input", "value"),
            State("graph-store", "data"),
        ],
        prevent_initial_call=True,
    )
    def generate_bridge_text(n_clicks, input_text, graph_text):
        if not n_clicks or not input_text or not graph_text:
            return "请先上传文本文件并输入要处理的文本。"

        try:
            # Create TextGraph instance from the stored graph data
            text_graph = TextGraph(graph_text)

            # Generate new text with bridge words
            result_text = text_graph.generate_text_with_bridges(input_text)

            # Use message template for consistent UI
            return bridge_text_result_message(input_text, result_text)
        except Exception as e:
            return bridge_text_result_message(input_text, f"处理错误: {str(e)}", is_error=True)
