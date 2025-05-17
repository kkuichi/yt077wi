import pandas as pd
import geopandas as gpd
import matplotlib.colors as mcolors
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc

def get_layout():
    # --------------------- PRVÝ GRAF: Kombinovaný barplot a scatterplot ---------------------
    data = pd.read_csv("data/NRSR2023_SK_tab03a.csv")
    df = pd.DataFrame(data)

    df = df.sort_values(by="Počet platných hlasov", ascending=False)

    # Vytvorenie Plotly stĺpcového grafu
    fig1 = go.Figure()

    fig1.add_trace(go.Bar(
        y=df["Názov politického subjektu"],
        x=df["Počet platných hlasov"],
        orientation='h',
        marker_color='rgba(93, 164, 214, 0.7)',
        name='Počet hlasov'
    ))

    fig1.add_trace(go.Scatter(
        y=df["Názov politického subjektu"],
        x=df["Počet platných hlasov"],
        mode='markers+text',
        text=[f"{val:.2f}%" for val in df["Podiel platných hlasov v %"]],
        textposition='middle right',
        marker=dict(color='red', size=10),
        name='Podiel hlasov'
    ))

    fig1.update_layout(
        title="Počet platných hlasov a podiel hlasov podľa politických subjektov",
        title_font=dict(size=24, family='Roboto', color='black', weight='bold'),
        xaxis_title="Počet platných hlasov",
        yaxis_title="Politický subjekt",
        height=700,
        margin=dict(l=100, r=50, t=100, b=50)
    )

    # --------------------- DRUHÝ GRAF: Víťazné strany podľa krajov ---------------------
    slovakia_map = gpd.read_file("app/Slovakia.geojson")
    slovakia_map = slovakia_map.rename(columns={"NM4": "region"})

    df2 = pd.read_csv("data/NRSR2023_SK_tab03b.csv")
    df2 = df2.rename(columns={"Názov kraja": "region"})

    # Získanie víťazov v krajoch
    df_max_votes = df2.loc[df2.groupby("region")["Počet platných hlasov"].idxmax()]
    df_map = slovakia_map.merge(df_max_votes, on="region", how="left")
    df_map['Názov kraja'] = df_map['region']

    # Farby podľa strán
    unique_parties = df_map['Názov politického subjektu'].dropna().unique()
    party_colors = dict(zip(unique_parties, mcolors.TABLEAU_COLORS.values()))
    df_map['color'] = df_map['Názov politického subjektu'].map(party_colors)
    df_map['color'] = df_map['color'].fillna("gray")

    geojson_data = df_map.__geo_interface__

    fig2 = px.choropleth_mapbox(
    df_map,
    geojson=geojson_data,
    locations='region',
    featureidkey='properties.region',
    color='Názov politického subjektu',
    color_discrete_map=party_colors,
    mapbox_style="white-bg",  
    center={"lat": 48.7, "lon": 19.7},
    zoom=6.2,
    opacity=0.9,
    title="Politické subjekty s najvyšším počtom hlasov podľa krajov",
    hover_name='Názov kraja',        
    hover_data={'region': False}     
)

    fig2.update_layout(
        title_font=dict(size=24, family='Roboto', color='black', weight='bold'),
        mapbox=dict(
            style="white-bg",
            center={"lat": 48.7, "lon": 19.7},
            zoom=6.2,
            pitch=0,
            bearing=0
        ),
        margin={"r":0,"t":80,"l":0,"b":0},
        height=600,
        legend_title="Víťaz v kraji",
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    return html.Div([
        html.H2("Preferencie politických subjektov a víťazi podľa krajov", style={
            'textAlign': 'center',
            'marginBottom': '40px',
            'marginTop': '20px',
            'fontFamily': 'Roboto',
            'color': 'black'
        }),
        dcc.Graph(figure=fig1),
        html.Hr(),
        dcc.Graph(figure=fig2)
    ])
