import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html, dash_table

# Načítanie mapových údajov
slovakia_map = gpd.read_file("app/Slovakia.geojson")
slovakia_map.rename(columns={"NM4": "region"}, inplace=True)

# Načítanie volebných údajov pre kraje
df = pd.read_csv("data/NRSR2023_SK_tab02a.csv")
df.rename(columns={"Názov kraja": "region"}, inplace=True)

# Načítanie volebných údajov pre okresy
df_districts = pd.read_csv("data/NRSR2023_SK_tab02c.csv")
df_districts.rename(columns={"Názov okresu": "district", "Účasť voličov v %": "turnout_percentage", "Názov kraja": "region"}, inplace=True)

# Spojenie volebných údajov s mapou krajov
df_map = slovakia_map.merge(df, on="region", how="left")

# Vytvorenie mapy krajov pomocou Plotly Graph Objects
fig = go.Figure(go.Choropleth(
    z=df_map["Účasť voličov v %"],
    hoverinfo="skip",  
    locations=df_map.index,
    locationmode="geojson-id",
    geojson=df_map.geometry.__geo_interface__,
    colorscale="OrRd",
    colorbar=dict(
        title="Volebná účasť (%)",
        tickvals=[0, 25, 50, 75, 100],
        ticktext=["0%", "25%", "50%", "75%", "100%"],
        tickmode="array"
    ),
    showscale=True
))

for idx, row in df_map.iterrows():
    if row["geometry"] is not None and not row["geometry"].is_empty:
        centroid = row.geometry.centroid
        lon = centroid.x
        lat = centroid.y

        # Manuálne posuny pre prekrývajúce sa kraje
        if row["region"] == "Bratislavský kraj":
            lon -= 0.1
            lat -= 0.1  
        elif row["region"] == "Trnavský kraj":
            lon += 0.1
            lat += 0.1  

        fig.add_trace(go.Scattergeo(
            locationmode="geojson-id",
            lon=[lon],
            lat=[lat],
            text=[f"{row['region']}<br>{row['Účasť voličov v %']:.1f}%"],
            showlegend=False,
            mode="text",
            textfont=dict(size=12, color="black", family="Roboto", weight="bold"),
            hoverinfo="text"
        ))

# Prispôsobenie vzhľadu mapy krajov
fig.update_geos(
    fitbounds="locations",
    visible=False,
    projection_type="mercator",
    showcoastlines=True,
    coastlinecolor="Black",
    projection_scale=20,  
    showcountries=False,
    showland=True
)

# Titulok a fonty pre mapu krajov
fig.update_layout(
    title="Volebná účasť podľa krajov",
    title_font=dict(size=24, family='Roboto', color='black', weight='bold'),
    geo=dict(showcoastlines=True, coastlinecolor="black"),
    font=dict(size=14, family='Roboto'),
    margin={"r":0, "t":50, "l":0, "b":0},
    dragmode=False,  
)

# Slovník s genitívnymi názvami krajov
genitive_names = {
    "Bratislavský kraj": "Bratislavského kraja",
    "Trnavský kraj": "Trnavského kraja",
    "Trenčiansky kraj": "Trenčianskeho kraja",
    "Nitriansky kraj": "Nitrianskeho kraja",
    "Žilinský kraj": "Žilinského kraja",
    "Banskobystrický kraj": "Banskobystrického kraja",
    "Prešovský kraj": "Prešovského kraja",
    "Košický kraj": "Košického kraja"
}

# Odstránenie "Cudziny" zo vstupných údajov
df_districts = df_districts[df_districts["region"] != "Cudzina"]

# Funkcia na vytvorenie jednej tabuľky
def generate_region_table(region_name):
    region_districts = df_districts[df_districts['region'] == region_name]
    region_districts = region_districts.sort_values(by="turnout_percentage", ascending=False)

    return dash_table.DataTable(
        id=f'district-table-{region_name}',
        columns=[
            {"name": "Okres", "id": "district"},
            {"name": "Volebná účasť (%)", "id": "turnout_percentage"}
        ],
        data=region_districts.to_dict('records'),
        style_table={'height': '400px', 'overflowY': 'auto', 'width': '100%'},
        style_cell={
            'textAlign': 'center',
            'fontFamily': 'Roboto',
            'padding': '8px',
            'fontSize': '14px'
        },
        style_header={
            'backgroundColor': '#5661DB',
            'color': 'white',
            'fontWeight': 'bold'
        },
        style_data={
            'backgroundColor': 'white',
            'color': 'black'
        }
    )

# Funkcia na rozloženie stránok s tabuľkami 
def generate_region_sections():
    region_sections = []
    regions = sorted([r for r in df['region'].unique() if r != "Cudzina"])  # zoradené abecedne
    
    for i in range(0, len(regions), 2):
        row = []
        for j in range(2):
            if i + j < len(regions):
                region = regions[i + j]
                gen_name = genitive_names.get(region, region)
                table = html.Div([
                    html.H3(f"Volebná účasť v okresoch {gen_name}", style={
                        'textAlign': 'center',
                        'fontFamily': 'Roboto',
                        'color': 'black',
                        'fontSize': '24px',
                        'fontWeight': 'bold'
                    }),
                    generate_region_table(region)
                ], style={'width': '48%', 'padding': '10px'})
                row.append(table)
        region_sections.append(html.Div(row, style={'display': 'flex', 'justifyContent': 'space-between'}))
    
    return region_sections

def get_layout():
    return html.Div([
        html.H2("Volebná účasť na Slovensku", style={
            'textAlign': 'center',
            'marginBottom': '40px',
            'marginTop': '20px',
            'fontFamily': 'Roboto',
            'color': 'black'
        }),

        html.Div([
            html.H3("Volebná účasť podľa krajov", style={
                'textAlign': 'center',
                'fontFamily': 'Roboto',
                'color': 'black'
            }),
            dcc.Graph(
                id='turnout-map',
                figure=fig,
                style={'height': '80vh', 'width': '100%', 'marginBottom': '40px'}
            )
        ], style={'padding': '20px'}),

        html.Hr(),

        html.H3("Volebná účasť podľa okresov v jednotlivých krajoch", style={
                'textAlign': 'center',
                'fontFamily': 'Roboto',
                'color': 'black'
        }),

        *generate_region_sections()
    ], style={'padding': '20px'})
