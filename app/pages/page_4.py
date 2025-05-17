import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html
from dash import dcc

# Načítanie údajov pre celé Slovensko
df_sr = pd.read_csv('data/NRSR2023_SK_tab07a.csv', usecols=['Názov politického subjektu', 'Počet platných prednostných hlasov']).copy()

# Agregácia počtu hlasov podľa politického subjektu
df_aggregated = df_sr.groupby('Názov politického subjektu', as_index=False).agg({'Počet platných prednostných hlasov': 'sum'})

# Získanie top 10 politických subjektov
top_10_subjekty = df_aggregated.sort_values(by='Počet platných prednostných hlasov', ascending=False).head(10)

# Použitie palety Viridis pre vizualizácie
colors = px.colors.sequential.Viridis

# Koláčový graf
fig_pie = px.pie(top_10_subjekty,
                 names='Názov politického subjektu',
                 values='Počet platných prednostných hlasov',
                 title='Top 10 politických subjektov podľa celkového počtu hlasov za celé Slovensko',
                 color='Názov politického subjektu',
                 hole=0.3,
                 color_discrete_sequence=colors)

fig_pie.update_layout(
    title_font=dict(size=24, family='Roboto', color='black', weight='bold'),
    plot_bgcolor="white",
    paper_bgcolor="white"
)

# Načítanie údajov pre kraje
df_kraje = pd.read_csv('data/NRSR2023_SK_tab07b.csv', usecols=['Názov kraja', 'Názov politického subjektu', 'Počet platných prednostných hlasov']).copy()

# Agregácia hlasov podľa kraja a politického subjektu
df_kraje_aggregated = df_kraje.groupby(['Názov kraja', 'Názov politického subjektu'], as_index=False).agg({'Počet platných prednostných hlasov': 'sum'})

df_sr_aggregated = df_kraje.groupby('Názov politického subjektu', as_index=False).agg({'Počet platných prednostných hlasov': 'sum'})

top_10_subjekty = df_sr_aggregated.sort_values(by='Počet platných prednostných hlasov', ascending=False).head(10)

df_kraje_top_10 = df_kraje_aggregated[df_kraje_aggregated['Názov politického subjektu'].isin(top_10_subjekty['Názov politického subjektu'])].copy()

# Agregácia hlasov podľa krajov
df_kraje_aggregated_by_total = df_kraje_top_10.groupby('Názov kraja', as_index=False).agg({'Počet platných prednostných hlasov': 'sum'})
df_kraje_aggregated_by_total = df_kraje_aggregated_by_total.sort_values(by='Počet platných prednostných hlasov', ascending=False)

# Udržanie správneho poradia politických subjektov
top_10_subjekty = top_10_subjekty.sort_values(by='Počet platných prednostných hlasov', ascending=True)

df_kraje_top_10['Názov kraja'] = pd.Categorical(
    df_kraje_top_10['Názov kraja'],
    categories=df_kraje_aggregated_by_total['Názov kraja'],
    ordered=True
)

df_kraje_top_10['Názov politického subjektu'] = pd.Categorical(
    df_kraje_top_10['Názov politického subjektu'],
    categories=top_10_subjekty['Názov politického subjektu'],
    ordered=True
)

df_kraje_top_10 = df_kraje_top_10.sort_values(by=['Názov kraja', 'Názov politického subjektu'], ascending=[True, False])

# Stĺpcový graf
fig_bar = px.bar(df_kraje_top_10,
                 x='Názov kraja',
                 y='Počet platných prednostných hlasov',
                 color='Názov politického subjektu',
                 title='Top 10 politických subjektov podľa celkového počtu hlasov v jednotlivých krajoch',
                 color_discrete_sequence=colors,
                 barmode='stack')

fig_bar.update_layout(
    title_font=dict(size=24, family='Roboto', color='black', weight='bold'),
    plot_bgcolor="white",
    paper_bgcolor="white"
)

# Načítanie údajov pre celé Slovensko
df_sr = pd.read_csv('data/NRSR2023_SK_tab07a.csv', usecols=['Meno', 'Priezvisko', 'Názov politického subjektu', 'Počet platných prednostných hlasov']).copy()

# Agregácia počtu hlasov podľa kandidáta
df_sr['Celé meno'] = df_sr['Meno'] + ' ' + df_sr['Priezvisko']
df_candidates = df_sr.groupby(['Celé meno', 'Názov politického subjektu'], as_index=False).agg({'Počet platných prednostných hlasov': 'sum'})

# Získanie top 10 kandidátov
top_10_kandidati = df_candidates.sort_values(by='Počet platných prednostných hlasov', ascending=False).head(10)

# Tabuľka top 10 kandidátov
table_fig = go.Figure(data=[go.Table(
    header=dict(values=['Celé meno', 'Názov politického subjektu', 'Počet platných prednostných hlasov'],
                fill_color='purple',
                align='left',
                font=dict(color='white', size=15)),
    cells=dict(values=[top_10_kandidati['Celé meno'], top_10_kandidati['Názov politického subjektu'], top_10_kandidati['Počet platných prednostných hlasov']],
               fill_color='lavender',
               align='left',
               font=dict(color='black', size=14))
)])

# Nastavenie názvu tabuľky
table_fig.update_layout(
    title='Top 10 kandidátov podľa počtu prednostných hlasov',  # Názov tabuľky
    title_font=dict(size=24, family='Roboto', color='black', weight='bold'),
    plot_bgcolor="white",
    paper_bgcolor="white"
)

# Názvy krajov pre správnu formu
kraj_names = {
    "Bratislavský kraj": "Bratislavskom kraji",
    "Trnavský kraj": "Trnavskom kraji",
    "Trenčiansky kraj": "Trenčianskom kraji",
    "Nitriansky kraj": "Nitrianskom kraji",
    "Žilinský kraj": "Žilinskom kraji",
    "Banskobystrický kraj": "Banskobystrickom kraji",
    "Prešovský kraj": "Prešovskom kraji",
    "Košický kraj": "Košickom kraji"
}

# Filtrácia krajov, aby sa zahrnuli len slovenské kraje
valid_kraje = ["Bratislavský kraj", "Trnavský kraj", "Trenčiansky kraj", "Nitriansky kraj", 
               "Žilinský kraj", "Banskobystrický kraj", "Prešovský kraj", "Košický kraj"]

# Načítanie kandidátov podľa krajov
df_kandidati_kraje = pd.read_csv('data/NRSR2023_SK_tab07b.csv', usecols=['Meno', 'Priezvisko', 'Názov politického subjektu', 'Počet platných prednostných hlasov', 'Názov kraja']).copy()

# Vytvorenie celého mena
df_kandidati_kraje['Celé meno'] = df_kandidati_kraje['Meno'] + ' ' + df_kandidati_kraje['Priezvisko']

# Filtrácia na platné kraje
df_kandidati_kraje = df_kandidati_kraje[df_kandidati_kraje['Názov kraja'].isin(valid_kraje)]

# Agregácia hlasov podľa kandidáta a kraja
df_kandidati_kraje_grouped = df_kandidati_kraje.groupby(['Názov kraja', 'Celé meno', 'Názov politického subjektu'], as_index=False).agg({
    'Počet platných prednostných hlasov': 'sum'
})

# Vytvorenie tabuliek pre každý kraj
krajinske_tabulky = []

for kraj in sorted(valid_kraje):
    df_kraj = df_kandidati_kraje_grouped[df_kandidati_kraje_grouped['Názov kraja'] == kraj].sort_values(by='Počet platných prednostných hlasov', ascending=False)

    df_kraj_top5 = df_kraj.head(5)

    table = go.Figure(data=[go.Table(
        header=dict(values=['Celé meno', 'Názov politického subjektu', 'Počet platných prednostných hlasov'],
                    fill_color='purple',
                    align='left',
                    font=dict(color='white', size=15)),
        cells=dict(values=[df_kraj_top5['Celé meno'], df_kraj_top5['Názov politického subjektu'], df_kraj_top5['Počet platných prednostných hlasov']],
                   fill_color='lavender',
                   align='left',
                   font=dict(color='black', size=14))
    )])

    kraj_name = kraj_names.get(kraj, kraj)

    table.update_layout(
        title=f'Top 5 kandidátov v {kraj_name}',  # Používame správny tvar názvu
        title_font=dict(size=20, family='Roboto', color='black', weight='bold'),
        margin=dict(t=50, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    krajinske_tabulky.append(dcc.Graph(figure=table))

# Layout pre Dash aplikáciu
def get_layout():
    return html.Div([
        html.H2("Analýza výsledkov politických subjektov a kandidátov", style={
            'textAlign': 'center',
            'marginBottom': '40px',
            'marginTop': '20px',
            'fontFamily': 'Roboto',
            'color': 'black'
        }),

        # Hlavné grafy
        dcc.Graph(figure=fig_pie),
        html.Hr(),

        dcc.Graph(figure=fig_bar),
        html.Hr(),

        dcc.Graph(figure=table_fig),  # Tabuľka pre celé Slovensko
        html.Hr(),

        html.H2("Top 5 kandidátov podľa počtu prednostných hlasov v jednotlivých krajoch", style={
            'textAlign': 'center',
            'marginTop': '40px',
            'marginBottom': '20px',
            'fontFamily': 'Roboto',
            'color': 'black'
        }),

        html.Div([
            html.Div(krajinske_tabulky[i], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'})
            for i in range(0, len(krajinske_tabulky))
        ], style={'display': 'flex', 'flexWrap': 'wrap'}),
    ], style={'padding': '20px'})
