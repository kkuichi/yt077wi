import pandas as pd
import plotly.express as px
from dash import html, dcc

# Načítanie dát
df = pd.read_csv('data/NRSR2023_SK_tab04.csv')

# Výber potrebných stľpcov
df = df[['Názov politického subjektu', 'Počet platných hlasov', 'Pridelené mandáty spolu', 'Počet kandidátov']]

# Usporiadanie podľa počtu hlasov
df = df.sort_values(by='Počet platných hlasov', ascending=False)

# Priradenie farieb
colors = px.colors.sequential.Viridis
color_map = {subjekt: colors[i % len(colors)] for i, subjekt in enumerate(df['Názov politického subjektu'])}

background_color = "#FFFFFF"
title_style = dict(size=24, family='Roboto', color='black', weight='bold')

# Stľpcový graf
fig_bar = px.bar(df,
                 x='Názov politického subjektu',
                 y='Pridelené mandáty spolu',
                 hover_data={'Počet platných hlasov': True},
                 labels={'Pridelené mandáty spolu': 'Počet mandátov'},
                 title='Počet mandátov pre politické subjekty',
                 color='Názov politického subjektu',
                 color_discrete_map=color_map)

fig_bar.update_traces(marker=dict(line=dict(width=1, color='black')), opacity=0.9)
fig_bar.update_layout(yaxis_title="Počet mandátov",
                      plot_bgcolor=background_color,
                      paper_bgcolor=background_color,
                      title_font=title_style)

# Koláčový graf
fig_pie = px.pie(df,
                 names='Názov politického subjektu',
                 values='Počet platných hlasov',
                 title='Percentuálne rozdelenie hlasov medzi subjekty',
                 color='Názov politického subjektu',
                 color_discrete_map=color_map,
                 hole=0.4)

fig_pie.update_traces(
    textinfo='percent+label',
    hoverinfo='label+percent+value',
    pull=[0.1 if x == df['Názov politického subjektu'].iloc[0] else 0 for x in df['Názov politického subjektu']]
)
fig_pie.update_layout(plot_bgcolor=background_color,
                      paper_bgcolor=background_color,
                      title_font=title_style)

# Scatter plot
fig_scatter = px.scatter(df,
                         x='Počet platných hlasov',
                         y='Pridelené mandáty spolu',
                         size='Počet kandidátov',
                         color='Názov politického subjektu',
                         title='Porovnanie počtu hlasov a získaných mandátov',
                         color_discrete_map=color_map,
                         hover_name='Názov politického subjektu')

fig_scatter.update_layout(xaxis_title="Počet platných hlasov",
                          yaxis_title="Počet mandátov",
                          plot_bgcolor=background_color,
                          paper_bgcolor=background_color,
                          title_font=title_style)

def get_layout():
    return html.Div([
        html.H2("Analýza mandátov a hlasovania", style={
            'textAlign': 'center',
            'marginBottom': '40px',
            'marginTop': '20px',
            'fontFamily': 'Roboto',
            'color': 'black'
        }),

        dcc.Graph(figure=fig_bar),
        html.Hr(),

        dcc.Graph(figure=fig_pie),
        html.Hr(),

        dcc.Graph(figure=fig_scatter),
    ], style={'padding': '20px'})
