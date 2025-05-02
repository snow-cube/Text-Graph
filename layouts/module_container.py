from dash import html

MODULE_CONTAINER_STYLE = {
    "padding": "10px",
    "marginBottom": "16px",
    "border": "1px solid #ddd",
    "backgroundColor": "#f9f9f9",
    "borderRadius": "8px",
    "boxShadow": "0 1px 3px rgba(0,0,0,0.08)",
}


def module_container(title, content_list, right_component=None):
    header_content = [
        html.H3(
            title,
            style={
                "margin": "0 10px 0 0",
                "display": "inline-block",
                "color": "#0e6165",
                "fontWeight": "bold",
                "fontSize": "16px",
                "flex": "0 0 auto",
            },
        )
    ]

    # Add right component if provided
    if right_component is not None:
        header_content.append(
            html.Div(
                right_component,
                style={"flex": "1", "textAlign": "right"},
            )
        )

    return html.Div(
        [
            html.Div(
                header_content,
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "marginBottom": "8px",
                    "paddingLeft": "4px",
                    "justifyContent": "space-between",
                },
            ),
            *content_list,
        ],
        style=MODULE_CONTAINER_STYLE,
    )


def container_line(content):
    return html.Div(
        content,
        style={
            "display": "flex",
            "alignItems": "center",
            "marginTop": "8px",
            "gap": "10px",
        },
    )
