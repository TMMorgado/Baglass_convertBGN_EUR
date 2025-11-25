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

    # Stores for each file type
    dcc.Store(id="store-converted-deklar"),
    dcc.Store(id="store-filename-deklar"),
    dcc.Store(id="store-encoding-deklar"),

    dcc.Store(id="store-converted-prodagbi"),
    dcc.Store(id="store-filename-prodagbi"),
    dcc.Store(id="store-encoding-prodagbi"),

    dcc.Store(id="store-converted-pokupki"),
    dcc.Store(id="store-filename-pokupki"),
    dcc.Store(id="store-encoding-pokupki"),


    # NAVBAR
    dbc.Navbar(
        dbc.Container([
            html.A(
                dbc.Row([
                    dbc.Col(
                        html.Img(
                            src="/assets/BAlogo.png",
                            height="40px",
                            className="logo"
                        ),
                        width="auto",
                        align="center"
                    ),
                    dbc.Col(
                        dbc.NavbarBrand(
                            "Glass Bulgaria",
                            className="mb-0 h4"
                        )
                    ),
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
                    html.P(
                        "Converting BGN values to EUR.",
                        className="lead mb-0"
                    )
                ], className="hero text-center")
            ], md=10, lg=8)
        ], className="justify-content-center")
    ], className="mt-4 mb-3"),

    # MAIN CARD – 3 uploads (Deklar, Prodagbi, Pokupki)
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card(className="containerCard glass-card mb-4", children=[

                    dbc.CardHeader(
                        html.Div([
                            html.I(className="bi bi-cloud-arrow-up-fill me-2"),
                            html.Span(
                                "Created for: Prodagbi, Pokupki and Deklar", className="fw-bold")
                        ],
                            className="d-flex align-items-center justify-content-center")
                    ),

                    dbc.CardBody(children=[

                        html.Div(
                            "Upload .txt Files",
                            className="text-muted text-center mb-4"
                        ),

                        dbc.Row(className="gy-4", children=[

                            # --- PRODAGBI COLUMN ---
                            dbc.Col(md=4, children=[
                                dbc.CardBody(className="border rounded p-3 h-100", children=[
                                    html.H5(
                                        "Prodagbi",
                                        className="fw-bold text-center mb-3"
                                    ),

                                    dcc.Upload(
                                        id="upload-prodagbi",
                                        children=html.Div([
                                            html.I(
                                                className="bi bi-upload me-2"),
                                            "Select prodagbi.txt"
                                        ],
                                            className="btn btn-primary btn-sm w-100"),
                                        multiple=False,
                                        className="upload-dropzone text-center"
                                    ),

                                    html.Small(
                                        "",
                                        className="text-muted d-block mt-2"
                                    ),

                                    html.Hr(),

                                    html.Div(
                                        id="file_status_prodagbi",
                                        className="text-body-secondary mt-2 small"
                                    ),

                                    html.Div(
                                        className="d-grid gap-2 mt-3",
                                        children=[
                                            html.Button(
                                                children=[
                                                    html.I(
                                                        className="bi bi-download me-2"),
                                                    "Download Prodagbi"
                                                ],
                                                id="download-btn-prodagbi",
                                                className="btn btn-success btn-sm",
                                                disabled=True,
                                            ),
                                            dcc.Download(
                                                id="download-out-prodagbi")
                                        ]
                                    ),
                                ])
                            ]),

                            # --- POKUPKI COLUMN ---
                            dbc.Col(md=4, children=[
                                dbc.CardBody(className="border rounded", children=[
                                    html.H5(
                                        "Pokupki",
                                        className="fw-bold text-center mb-3"
                                    ),

                                    dcc.Upload(
                                        id="upload-pokupki",
                                        children=html.Div([
                                            html.I(
                                                className="bi bi-upload me-2"),
                                            "Select pokupki.txt"
                                        ],
                                            className="btn btn-primary btn-sm w-100"),
                                        multiple=False,
                                        className="upload-dropzone text-center"
                                    ),

                                    html.Small(
                                        "",
                                        className="text-muted d-block mt-2"
                                    ),

                                    html.Hr(),

                                    html.Div(
                                        id="file_status_pokupki",
                                        className="text-body-secondary mt-2 small"
                                    ),

                                    html.Div(
                                        className="d-grid gap-2 mt-3",
                                        children=[
                                            html.Button(
                                                children=[
                                                    html.I(
                                                        className="bi bi-download me-2"),
                                                    "Download Pokupki"
                                                ],
                                                id="download-btn-pokupki",
                                                className="btn btn-success btn-sm",
                                                disabled=True,
                                            ),
                                            dcc.Download(
                                                id="download-out-pokupki")
                                        ]
                                    ),
                                ])
                            ]),
                            # --- DEKLAR COLUMN ---
                            dbc.Col(md=4, children=[
                                dbc.CardBody(className="border rounded p-3 h-100", children=[
                                    html.H5(
                                        "Deklar",
                                        className="fw-bold text-center mb-3"
                                    ),

                                    dcc.Upload(
                                        id="upload-deklar",
                                        children=html.Div([
                                            html.I(
                                                className="bi bi-upload me-2"),
                                            "Select deklar.txt"
                                        ],
                                            className="btn btn-primary btn-sm w-100"),
                                        multiple=False,
                                        className="upload-dropzone text-center",
                                        disabled=True  # <= start disabled
                                    ),

                                    html.Small(
                                        "",
                                        className="text-muted d-block mt-2"
                                    ),

                                    html.Hr(),

                                    html.Div(
                                        id="file_status_deklar",
                                        className="text-body-secondary mt-2 small"
                                    ),

                                    html.Div(
                                        className="d-grid gap-2 mt-3",
                                        children=[
                                            html.Button(
                                                children=[
                                                  html.I(
                                                      className="bi bi-download me-2"),
                                                  "Download Deklar"
                                                ],
                                                id="download-btn-deklar",
                                                className="btn btn-success btn-sm",
                                                disabled=True  # <= start disabled
                                            ),

                                            dcc.Download(
                                                id="download-out-deklar")
                                        ]
                                    ),
                                ])
                            ]),
                        ])
                    ])
                ])
            ], className="containerCard d-flex justify-content-center")
        ], className="justify-content-center gy-4")
    ], className="mb-5"),

    # FOOTER
    dbc.Container([
        html.Hr(),
        dbc.Row([
            dbc.Col(
                html.Small(f"© {pd.Timestamp.now().year} • BA Glass"),
                md="auto"
            ),
            dbc.Col(html.Small(), md="auto")
        ], className="g-3 justify-content-center text-center")
    ], className="mb-4")

], className="app-wrapper")


# ------------- CALLBACKS -------------

# decoding files
def _decode_contents(contents):
    if not contents:
        raise PreventUpdate
    try:
        _, content_b64 = contents.split(",", 1)
        raw = base64.b64decode(content_b64)
    except Exception:
        return None, None, None
    enc, text = co.try_decode_bytes(raw)
    return raw, enc, text

# ---- DEKLAR ----
# upload


@app.callback(
    Output("file_status_deklar", "children"),
    Output("store-converted-deklar", "data"),
    Output("store-filename-deklar", "data"),
    Output("store-encoding-deklar", "data"),
    Input("upload-deklar", "contents"),
    State("upload-deklar", "filename"),
    prevent_initial_call=True
)
def on_upload_deklar(contents, filename):

    if filename == "deklar.txt":
        raw, enc, text = _decode_contents(contents)
        if raw is None:
            return "Failed to read file.", None, None, None

        converted = co.convert_deklar(text)
        msg = f'Loaded "{filename}" · Encoding: {enc} · Length: {len(text)} chars'
        return msg, converted, (filename or "deklar.txt"), enc

    return "Error: file is not deklar.txt", None, None, None
# download


@app.callback(
    Output("download-out-deklar", "data"),
    Input("download-btn-deklar", "n_clicks"),
    State("store-converted-deklar", "data"),
    State("store-filename-deklar", "data"),
    State("store-encoding-deklar", "data"),
    prevent_initial_call=True
)
def on_download_deklar(n, converted, filename, enc):
    if not n:
        raise PreventUpdate
    if not converted:
        raise PreventUpdate

    base = (filename or "deklar.txt").rsplit(".", 1)[0]
    enc = enc or "utf-8"

    def writer(buf):
        buf.write(converted.encode(enc, errors="strict"))

    return dcc.send_bytes(writer, filename=f"{base}_EUR.txt")


# ---- PRODAGBI ----
# upload
@app.callback(
    Output("file_status_prodagbi", "children"),
    Output("store-converted-prodagbi", "data"),
    Output("store-filename-prodagbi", "data"),
    Output("store-encoding-prodagbi", "data"),
    Input("upload-prodagbi", "contents"),
    State("upload-prodagbi", "filename"),
    prevent_initial_call=True
)
def on_upload_prodagbi(contents, filename):

    if filename.casefold() == "prodagbi.txt":
        raw, enc, text = _decode_contents(contents)
        if raw is None:
            return "Failed to read file.", None, None, None

        converted = co.convert_prodagbi(text)
        msg = f'Loaded "{filename}" · Encoding: {enc} · Length: {len(text)} chars'
        return msg, converted, (filename or "prodagbi.txt"), enc

    return "Error: file is not prodagbi.txt", None, None, None
# download


@app.callback(
    Output("download-out-prodagbi", "data"),
    Input("download-btn-prodagbi", "n_clicks"),
    State("store-converted-prodagbi", "data"),
    State("store-filename-prodagbi", "data"),
    State("store-encoding-prodagbi", "data"),
    prevent_initial_call=True
)
def on_download_prodagbi(n, converted, filename, enc):
    if not n:
        raise PreventUpdate
    if not converted:
        # No file converted yet -> do nothing
        raise PreventUpdate

    base = (filename or "prodagbi.txt").rsplit(".", 1)[0]
    enc = enc or "utf-8"

    def writer(buf):
        buf.write(converted.encode(enc, errors="strict"))

    return dcc.send_bytes(writer, filename=f"{base}_EUR.txt")


# ---- POKUPKI ----
# upload
@app.callback(
    Output("file_status_pokupki", "children"),
    Output("store-converted-pokupki", "data"),
    Output("store-filename-pokupki", "data"),
    Output("store-encoding-pokupki", "data"),
    Input("upload-pokupki", "contents"),
    State("upload-pokupki", "filename"),
    prevent_initial_call=True
)
def on_upload_pokupki(contents, filename):

    if filename.casefold() == "pokupki.txt":  # VERIFICAR COM O PAULO SE VALE A PENA TER VERIFICACAO NOME FICHEIRO
        raw, enc, text = _decode_contents(contents)
        if raw is None:
            return "Failed to read file.", None, None, None
        converted = co.convert_pokupki(text)
        msg = f'Loaded "{filename}" · Encoding: {enc} · Length: {len(text)} chars'
        return msg, converted, (filename or "pokupki.txt"), enc

    return "Error: file is not pokupki.txt", None, None, None
# download


@app.callback(
    Output("download-out-pokupki", "data"),
    Input("download-btn-pokupki", "n_clicks"),
    State("store-converted-pokupki", "data"),
    State("store-filename-pokupki", "data"),
    State("store-encoding-pokupki", "data"),
    prevent_initial_call=True
)
def on_download_pokupki(n, converted, filename, enc):
    if not n:
        raise PreventUpdate
    if not converted:
        raise PreventUpdate

    base = (filename or "pokupki.txt").rsplit(".", 1)[0]
    enc = enc or "utf-8"

    def writer(buf):
        buf.write(converted.encode(enc, errors="strict"))

    return dcc.send_bytes(writer, filename=f"{base}_EUR.txt")


# *****toggle btn download*****
# btn deklar
@app.callback(
    Output("download-btn-deklar", "disabled"),
    Input("store-converted-prodagbi", "data"),
    Input("store-converted-pokupki", "data"),
    Input("store-converted-deklar", "data"),
)
def toggle_deklar_download_button(converted_prodagbi, converted_pokupki, converted_deklar):

    if not converted_prodagbi or not converted_pokupki or not converted_deklar:
        return True  # disabled

    return False  # enabled


@app.callback(
    Output("upload-deklar", "disabled"),
    Input("store-converted-prodagbi", "data"),
    Input("store-converted-pokupki", "data"),
)
def toggle_deklar_download_button(converted_prodagbi, converted_pokupki):

    if not converted_prodagbi or not converted_pokupki:
        return True  # disabled

    return False  # enabled

# btn Prodagbi


@app.callback(
    Output("download-btn-prodagbi", "disabled"),
    Input("store-converted-prodagbi", "data"),
)
def toggle_prodagbi_download_button(converted_prodagbi):

    if not converted_prodagbi:
        return True  # disabled

    return False  # enabled

# btn Pokupki


@app.callback(
    Output("download-btn-pokupki", "disabled"),
    Input("store-converted-pokupki", "data"),
)
def toggle_pokupki_download_button(converted_pokupki):

    if not converted_pokupki:
        return True  # disabled

    return False  # enabled
# ***** end toggle btn download*****


if __name__ == "__main__":
    app.run(debug=False)
