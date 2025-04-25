from dash import Output, Input
import dash


def register_image_callback(app):
    @app.callback(
        Output("cytoscape", "generateImage"),
        Input("save-image-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def save_cytoscape_image(n_clicks):
        if n_clicks:
            return {
                "type": "png",
                "action": "download",
                "filename": "graph.png",
                "width": 1200,
                "height": 800,
                "scale": 2,
            }
        return dash.no_update
