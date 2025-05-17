import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc

# --- Graf 1: Stredný vek kandidátov ---
vek_df = pd.read_csv('data/NRSR2023_SK_tab0d.csv')
stredny_vek = round(vek_df['Priemerný vek'].mean(), 1)

vek_fig = go.Figure(data=[go.Bar(
    x=["Stredný vek"], 
    y=[stredny_vek],
    marker_color="#5661DB"
)])
vek_fig.update_layout(
    title="Stredný vek kandidátov",
    title_font=dict(size=24, family='Roboto', color='black', weight='bold'),
    yaxis=dict(range=[0, 100]),
    xaxis=dict(title="Kategória"),
    yaxis_title="Vek (roky)",
)

# --- Graf 2: Podiel kandidátov s titulom ---
tituly_df = pd.read_csv('data/NRSR2023_SK_tab0b.csv')
tituly_df['Titul'] = tituly_df['Titul'].apply(lambda x: 'S titulom' if pd.notna(x) else 'Bez titulu')
title_counts = tituly_df['Titul'].value_counts()

tituly_fig = go.Figure(data=[go.Pie(
    labels=title_counts.index,
    values=title_counts.values,
    marker=dict(colors=['#5661DB', '#9FB7DB']),
    textinfo='percent+label'
)])
tituly_fig.update_layout(
    title="Pomer kandidátov s titulom a bez titulu",
    title_font=dict(size=24, family='Roboto', color='black', weight='bold')
)

# --- Graf 3: Najčastejšie akademické tituly (Top 5) ---
top_titles = pd.read_csv('data/NRSR2023_SK_tab0b.csv')['Titul'].value_counts().nlargest(5)

top_titles_fig = go.Figure(data=[go.Bar(
    x=top_titles.index,
    y=top_titles.values,
    marker_color=['#5661DB', '#7C85E0', '#9FB7DB', '#BDC9E8', '#D1D8F1']  # Rôzne odtiene modrej
)])
top_titles_fig.update_layout(
    title="Počet kandidátov podľa titulov (Top 5)",
    title_font=dict(size=24, family='Roboto', color='black', weight='bold'),
    xaxis_title="Akademický titul",
    yaxis_title="Počet kandidátov",
    xaxis_tickangle=-45,
    yaxis=dict(range=[0, top_titles.max() + 10])
)

# --- Graf 4: Podiel mužov a žien ---
candidates_df = pd.read_csv('data/NRSR2023_SK_tab0b.csv')
elected_df = pd.read_csv('data/NRSR2023_SK_tab06.csv')

def estimate_gender(name):
    return 'Žena' if isinstance(name, str) and name.endswith('a') else 'Muž'

candidates_df['Pohlavie'] = candidates_df['Meno'].apply(estimate_gender)
elected_df['Pohlavie'] = elected_df['Meno'].apply(estimate_gender)

gender_counts_candidates = candidates_df['Pohlavie'].value_counts().reindex(['Muž', 'Žena'])
gender_counts_elected = elected_df['Pohlavie'].value_counts().reindex(['Muž', 'Žena'])

# Kandidáti
gender_candidates_fig = go.Figure(data=[go.Pie(
    labels=gender_counts_candidates.index,
    values=gender_counts_candidates.values,
    marker=dict(colors=['#5661DB', '#DB6B79']),
    textinfo='percent+label'
)])
gender_candidates_fig.update_layout(
    title="Kandidáti: podiel mužov a žien",
    title_font=dict(size=24, family='Roboto', color='black', weight='bold')
)

# Zvolení
gender_elected_fig = go.Figure(data=[go.Pie(
    labels=gender_counts_elected.index,
    values=gender_counts_elected.values,
    marker=dict(colors=['#5661DB', '#DB6B79']),
    textinfo='percent+label'
)])
gender_elected_fig.update_layout(
    title="Zvolení poslanci: podiel mužov a žien",
    title_font=dict(size=24, family='Roboto', color='black', weight='bold')
)

# --- Graf 5: Top 5 zamestnaní ---
top_jobs = candidates_df['Zamestnanie'].value_counts().nlargest(5)

top_jobs_fig = go.Figure(data=[go.Bar(
    x=top_jobs.index,
    y=top_jobs.values,
    marker_color=['#5661DB', '#7C85E0', '#9FB7DB', '#BDC9E8', '#D1D8F1'],  # Rôzne odtiene modrej
    text=top_jobs.values,
    textposition='outside'
)])
top_jobs_fig.update_layout(
    title="Počet kandidátov podľa zamestnania (Top 5)",
    title_font=dict(size=24, family='Roboto', color='black', weight='bold'),
    xaxis_title="Zamestnanie",
    yaxis_title="Počet kandidátov",
    xaxis_tickangle=-45
)

# --- Graf 6: Top 10 obcí ---
municipality_counts = candidates_df['Obec trvalého pobytu'].value_counts().nlargest(10)

top_municipalities_fig = go.Figure(data=[go.Bar(
    x=municipality_counts.index,
    y=municipality_counts.values,
    marker_color=['#5661DB', '#7C85E0', '#9FB7DB', '#BDC9E8', '#D1D8F1', '#A3B4D9', '#9FB7DB', '#7C85E0', '#5661DB', '#D1D8F1'],
    text=municipality_counts.values,
    textposition='outside'
)])
top_municipalities_fig.update_layout(
    title="Top 10 obcí podľa počtu kandidátov",
    title_font=dict(size=24, family='Roboto', color='black', weight='bold'),
    xaxis_title="Obec",
    yaxis_title="Počet kandidátov",
    xaxis_tickangle=-45
)

def get_layout():
    return html.Div([
        html.H2("Charakteristiky kandidátov NRSR 2023", style={
            'textAlign': 'center',
            'marginBottom': '40px',
            'marginTop': '20px',
            'fontFamily': 'Roboto',
            'color': 'black'
        }),

        dcc.Graph(figure=vek_fig),
        html.Hr(),

        dcc.Graph(figure=tituly_fig),
        html.Hr(),

        dcc.Graph(figure=top_titles_fig),
        html.Hr(),

        dcc.Graph(figure=gender_candidates_fig),
        html.Hr(),

        dcc.Graph(figure=gender_elected_fig),
        html.Hr(),

        dcc.Graph(figure=top_jobs_fig),
        html.Hr(),

        dcc.Graph(figure=top_municipalities_fig),
    ], style={'padding': '20px'})