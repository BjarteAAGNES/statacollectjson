from dash import Input, Output, html
import json
import base64
import io
import dash_bootstrap_components as dbc
from utils.utils import fetch_json_from_source, json_to_accordion

def register_callbacks(app):
    @app.callback(
        Output("json-accordion", "children"),
        Output("layout-info", "children"),
        Input("json-source", "value"),
        Input("include-regex", "value"),
        Input("exclude-regex", "value"),
        Input("omit-base", "value"),
        Input('upload-json', 'contents')
    )
    def update_view(json_source, include_regex, exclude_regex, omit_base, uploaded_contents):
        if uploaded_contents is not None:
            content_type, content_string = uploaded_contents.split(',')
            decoded = base64.b64decode(content_string)
            try:
                data = json.load(io.StringIO(decoded.decode('utf-8')))
            except Exception as e:
                data = {"error": f"Failed to parse uploaded JSON file: {e}"}
        else:
            data = fetch_json_from_source(json_source)

        accordion = json_to_accordion(data, include_regex, exclude_regex, omit_base)

        layout_info = []
        layout_dict = data.get("Layout", {})
        if isinstance(layout_dict, dict):
            for k, v in layout_dict.items():
                layout_info.append(html.Div(f"{k}: {v}"))
        elif isinstance(layout_dict, str):
            layout_info.append(html.Div(layout_dict))

        return accordion, layout_info
