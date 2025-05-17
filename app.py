import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from pages import page_1, page_2, page_3, page_4, page_5, page_6
from dash.exceptions import PreventUpdate

# Inicializácia aplikácie
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

# Pomocná funkcia na generovanie URL
def generate_url(page_name):
    return f"/{page_name}" if page_name != "home" else "/"

# Layout aplikácie
app.layout = html.Div([
    dbc.NavbarSimple(
        children=[],  
        id="navbar-links",
        brand="Generovanie štatistík a vizualizácií",
        brand_href=generate_url("home"),
        color="primary",
        dark=True,
    ),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callback na zmenu odkazu v navigácii podľa aktuálnej stránky
@app.callback(
    Output('navbar-links', 'children'),
    [Input('url', 'pathname')]
)

def update_navbar(pathname):
    links = [
        dbc.NavItem(dbc.NavLink("Domov", href=generate_url("home"), active="exact" if pathname == "/" else None)),
        dbc.NavItem(dbc.NavLink("Strana 1", href=generate_url("page-1"), active="exact" if pathname == "/page-1" else None)),
        dbc.NavItem(dbc.NavLink("Strana 2", href=generate_url("page-2"), active="exact" if pathname == "/page-2" else None)),
        dbc.NavItem(dbc.NavLink("Strana 3", href=generate_url("page-3"), active="exact" if pathname == "/page-3" else None)),
        dbc.NavItem(dbc.NavLink("Strana 4", href=generate_url("page-4"), active="exact" if pathname == "/page-4" else None)),
        dbc.NavItem(dbc.NavLink("Strana 5", href=generate_url("page-5"), active="exact" if pathname == "/page-5" else None)),
        dbc.NavItem(dbc.NavLink("Strana 6", href=generate_url("page-6"), active="exact" if pathname == "/page-6" else None)),
    ]
    return links

# Funkcia na vytvorenie navigačných tlačidiel "Späť" a "Ďalej"
def navigation_buttons(next_page, prev_page=None):
    buttons = []

    if prev_page:
        buttons.append(
            dcc.Link(
                html.Button("⬅️ Späť", style={
                    'margin': '10px',
                    'padding': '10px 20px',
                    'fontWeight': 'bold',
                    'backgroundColor': '#9FB7DB',
                    'border': 'none',
                    'borderRadius': '5px',
                    'cursor': 'pointer'
                }),
                href=generate_url(prev_page)
            )
        )

    if next_page:
        buttons.append(
            dcc.Link(
                html.Button("➡️ Ďalej", style={
                    'margin': '10px',
                    'padding': '10px 20px',
                    'fontWeight': 'bold',
                    'backgroundColor': '#5661DB',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '5px',
                    'cursor': 'pointer'
                }),
                href=generate_url(next_page)
            )
        )

    return html.Div(buttons, style={'textAlign': 'center', 'marginTop': '30px', 'marginBottom': '30px'})

# Callback pre dynamický obsah stránky
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    styles = {
        'container': {
            'max-width': '900px', 'margin': 'auto', 'padding': '50px',
            'backgroundColor': '#f8f9fa', 'borderRadius': '10px'
        },
        'title': {
            'textAlign': 'center', 'color': '#5661DB', 'fontSize': '36px', 'fontWeight': 'bold'
        },
        'sectionTitle': {
            'textAlign': 'center', 'fontSize': '28px', 'color': '#5661DB'
        },
        'paragraph': {
            'textAlign': 'center', 'fontSize': '20px', 'maxWidth': '900px',
            'marginLeft': 'auto', 'marginRight': 'auto'
        },
        'button': {
            'backgroundColor': '#5661DB', 'border': 'none', 'padding': '10px 20px', 'fontSize': '18px', 'cursor': 'pointer'
        },
        'buttonContainer': {
            'textAlign': 'center', 'paddingTop': '30px'
        }
    }

    if pathname == '/' or pathname == '/home':
        return html.Div([
            html.H1("Generovanie štatistík a vizualizácií z kandidátskych listín do volieb", style=styles['title']),
            html.P(
                "Táto aplikácia je zameraná na analýzu a vizualizáciu údajov z volieb do Národnej rady Slovenskej republiky (NRSR) 2023. "
                "Cieľom je poskytnúť prehľadné štatistiky a vizualizácie, ktoré umožnia lepšie pochopenie výsledkov volieb a analýzu preferencií kandidátov a politických strán.",
                style=styles['paragraph']
            ),
            html.P(
                "Voľby sú jedným z kľúčových pilierov demokratických procesov a ich výsledky ovplyvňujú politickú krajinu na mnoho rokov dopredu. "
                "Aby sme mohli správne interpretovať výsledky, je dôležité analyzovať ich v širšom kontexte. Vizualizácie nám umožňujú nielen rýchlo zachytiť dôležité trendy a vzory v údajoch, "
                "ale aj porovnať jednotlivé volebné obvody, kandidátov a politické strany.",
                style=styles['paragraph']
            ),
            html.Div([
                html.H3("Prečo vizualizovať dáta?", style=styles['sectionTitle']),
                html.P(
                    "Vizualizácia údajov je neoceniteľná pri analýze veľkých množstiev informácií. Pomáha nám efektívne prezentovať zložité štatistiky a faktory v jednoducho pochopiteľnom formáte, "
                    "čo umožňuje rýchlu analýzu a rozhodovanie. V kontexte volieb, vizualizácie ukazujú nielen celkové výsledky, ale aj trendy na regionálnej úrovni, "
                    "čo poskytuje hlbší pohľad na volebné správanie obyvateľstva.",
                    style=styles['paragraph']
                )
            ], style={'padding': '40px'}),
            html.Div([
                html.Hr(),
                html.Div([
                    dcc.Link(
                        html.Button("Prejsť na vizualizácie", className="btn btn-primary", style=styles['button']),
                        href=generate_url("page-1")
                    )
                ], style=styles['buttonContainer'])
            ], style={'maxWidth': '900px', 'margin': 'auto'})
        ], style=styles['container'])

    elif pathname == '/page-1':
        return html.Div([
            page_1.get_layout(),
            navigation_buttons(next_page='page-2', prev_page='home')
        ])

    elif pathname == '/page-2':
        return html.Div([
            page_2.get_layout(),
            navigation_buttons(next_page='page-3', prev_page='page-1')
        ])

    elif pathname == '/page-3':
        return html.Div([
            page_3.get_layout(),
            navigation_buttons(next_page='page-4', prev_page='page-2')
        ])

    elif pathname == '/page-4':
        return html.Div([
            page_4.get_layout(),
            navigation_buttons(next_page='page-5', prev_page='page-3')
        ])

    elif pathname == '/page-5':
        return html.Div([
            page_5.get_layout(),
            navigation_buttons(next_page='page-6', prev_page='page-4')
        ])

    elif pathname == '/page-6':
        return html.Div([
            page_6.get_layout(),
            navigation_buttons(next_page=None, prev_page='page-5')  # posledná strana – bez ďalšieho odkazu
        ])

    else:
        return html.Div([html.H1("404: Stránka neexistuje")])
    

# Callback funkcia na aktualizáciu mapy a tabuliek na strane 3
@app.callback(
    Output("mapa-obrazok", "src"),
    Output("tabulky-kraje", "children"),
    Input("subjekt-dropdown", "value")
)
def aktualizuj_mapu_a_tabulky(subjekt):
    if not subjekt:
        raise PreventUpdate
    mapa = page_3.zobraz_mapu(subjekt)
    tabulky = page_3.vytvor_tabulky(subjekt)  
    return mapa, tabulky

# Spustenie aplikácie
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host='0.0.0.0', port=port)