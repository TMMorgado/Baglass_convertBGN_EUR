import base64
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, no_update
from dash.exceptions import PreventUpdate
import convert as co


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.title = "BGN-EUR Converter"

app.layout = dbc.Container(fluid=True, children=[
    # Stores
    dcc.Store(id="store-converted"),
    dcc.Store(id="store-filename"),
     dcc.Store(id="store-encoding"),

    # NAVBAR
    dbc.Navbar(
        dbc.Container([
            html.A(
                dbc.Row([
                     dbc.Col(
                html.Img(src="/assets/BAlogo.png",
                         height="40px", className="logo"),
                width="auto",
                align="center"
            ),
                    dbc.Col(dbc.NavbarBrand(
                        "Glass Bulgaria", className="mb-0 h4")),
                ], align="center", className="g-0"),
                className="navbar-brand d-flex align-items-center"
            ),
            dbc.Nav([
                dbc.Badge("BGN → EUR", color="primary", className="me-2"),
                dbc.Badge("1 EUR = 1.95583 BGN", color="secondary"),
            ], className="ms-auto")
        ]),
        color="dark",
        dark=True,
        className="shadow-sm sticky-top"
    ),

    # HEADER / HERO
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1("Convert", className="fw-bold mb-2"),
                    html.P("Converting BGN values to EUR.",
                           className="lead mb-0")
                ], className="hero text-center")
            ], md=10, lg=8)
        ], className="justify-content-center")
    ], className="mt-4 mb-3"),

    # MAIN CARD
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card(className="containerCard glass-card mb-4", children=[
                    dbc.CardHeader([
                        html.Div([
                            html.I(className="bi bi-cloud-arrow-up-fill me-2"),
                            html.Span("Upload File", className="fw-bold")
                        ], className="d-flex align-items-center justify-content-center")
                    ]),
                    dbc.CardBody(className="text-center", children=[

                        # Upload button
                        dcc.Upload(
                            id="upload",
                            children=html.Div([
                                html.I(className="bi bi-upload me-2"),
                                "Select .txt"
                            ], className="btn btn-primary btn-lg"),
                            className="upload-dropzone mt-3",
                            multiple=False
                        ),
                        html.Small("Supports text files (.txt)",
                                   className="text-muted d-block mt-2"),

                        html.Hr(),

                        # Status + Alerts
                        html.Div(id="file_status",
                                 className="text-body-secondary mt-2"),
                        html.Div(id="alert-container", className="mt-3"),
                        dcc.Interval(id="alert-timer", interval=2000,
                                     n_intervals=0, disabled=True),
                                     

                        # Download 
                        html.Div(className="d-grid gap-2 mt-4", children=[
                            html.Button(
                                children=[
                                    html.I(className="bi bi-download me-2"), "Download"],
                                id="download-btn",
                                className="btn btn-success btn-lg"
                            ),
                            dcc.Download(id="download-out")
                        ]),

                        html.Div(className="mt-4 d-flex justify-content-center align-items-center", children=[
                            html.I(className="bi bi-info-circle me-2"),
                            html.Small("Created for: Deklar, Pokupki and Prodagbi",
                                       className="text-muted infoRate m-0")
                        ])
                    ])
                ])
            ], className="containerCard d-flex justify-content-center")
        ], className="justify-content-center gy-4")
    ], className=" mb-5"),

    # FOOTER
    dbc.Container([
        html.Hr(),
        dbc.Row([
            dbc.Col(html.Small(
                f"© {pd.Timestamp.now().year} • BA Glass"), md="auto"),
            dbc.Col(html.Small(), md="auto")
        ], className="g-3 justify-content-center text-center")
    ], className="mb-4")

], className="app-wrapper")

#Upload File
@app.callback(
    Output("file_status", "children", allow_duplicate=True),
    Output("store-converted", "data"),
    Output("store-filename", "data"),
    Output("store-encoding", "data"),
    Input("upload", "contents"),
    State("upload", "filename"),
    prevent_initial_call=True
)
def on_upload(contents, filename):
    if not contents:
        raise PreventUpdate
    try:
        _, content_b64 = contents.split(",", 1)
        raw = base64.b64decode(content_b64)
    except Exception:
        return ("Failed to read file.", None, None, None)

    enc, text = co.try_decode_bytes(raw)
    converted = co.convert_text_preserving_layout(text)

    msg = f'Loaded "{filename}" · Encoding: {enc} · Length: {len(text)} chars'
    return msg, converted, (filename or "file.txt"), enc

#Download new File
@app.callback(
    Output("download-out", "data"),
    Output("file_status", "children", allow_duplicate=True),
    Input("download-btn", "n_clicks"),
    State("store-converted", "data"),
    State("store-filename", "data"),
    State("store-encoding", "data"),
    prevent_initial_call=True
)
def on_download(n, converted, filename, enc):
    if not n:
        raise PreventUpdate
    if not converted:
        return no_update, "Nothing to download yet."
    base = (filename or "file.txt").rsplit(".", 1)[0]
    enc = enc or "utf-8"

    def writer(buf):
        buf.write(converted.encode(enc, errors="strict"))

    return dcc.send_bytes(writer, filename=f"{base}_EUR.txt"), ""


if __name__ == "__main__":
    app.run(debug=False)
