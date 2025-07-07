from dash import Dash
import dash_bootstrap_components as dbc

from layout.layout import create_layout
from callbacks.callbacks import register_callbacks

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "StataCollectJSON"
app.layout = create_layout()
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
