from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout():
    return dbc.Container([
        html.H2("📂 Stata graph collection viewer", className="my-3"),

        # Info textbox below title
        html.Div(
            "Browse a Stata graph collection JSON definition. Default filtering is derived from layout showing only data related to statistics defined in results, omiting base levels.",
            style={"marginBottom": "1rem", "fontStyle": "italic", "color": "#555"}
        ),

        dbc.Row([
            dbc.Col([
                dbc.Label("Enter JSON Source URL or File Path"),
                dcc.Input(
                    id="json-source",
                    type="text",
                    value="https://gist.githubusercontent.com/BjarteAAGNES/340ff8db8f85009f9239ef52714f75e4/raw/1d44f0a77db48ace350f62391137e09f7bedc7b9/tests.json",
                    style={"width": "100%", "marginBottom": "1rem"},
                    debounce=True,
                    placeholder="Enter URL or file path"
                ),

                dcc.Upload(
                    id='upload-json',
                    children=html.Div(['Drag and Drop or ', html.A('Select a JSON file')]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'marginBottom': '1rem'
                    },
                    multiple=False,
                ),

            ], width=12),
        ]),
        dbc.Row([
            dbc.Col([
                html.H5("Layout Information"),
                html.Div(id="layout-info", style={"marginBottom": "2rem"})
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Checkbox(
                    id="omit-base", value=True,
                    label="Omit Items with omit-type = 'base'",
                    label_style={"marginLeft": "0.5rem"},
                ),
                dbc.Label("Include Regex (filter to include keys matching)"),
                dcc.Input(id="include-regex", type="text", value=r"_r_b|_r_se", debounce=True, style={"width": "100%"}),
                html.Br(), html.Br(),
                dbc.Label("Exclude Regex (filter to exclude keys matching)"),
                dcc.Input(id="exclude-regex", type="text", debounce=True, style={"width": "100%"}),
            ], width=12)
        ]),
        html.Hr(),
        dbc.Accordion(id="json-accordion", flush=True, always_open=True)
    ], fluid=True)
