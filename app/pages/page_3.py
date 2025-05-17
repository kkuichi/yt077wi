import matplotlib
matplotlib.use('Agg')  
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import io
import base64
from dash import dcc, html
from dash.exceptions import PreventUpdate
from dash import dash_table

# Načítanie CSV s volebnými výsledkami
csv_path = "data/NRSR2023_SK_tab03b.csv"
data = pd.read_csv(csv_path)

# Načítanie GeoJSON súboru s hranicami krajov Slovenska
geojson_path = "app/Slovakia.geojson"
geo_data = gpd.read_file(geojson_path)

# Premenovanie stĺpcov pre správne zlúčenie
geo_data = geo_data.rename(columns={"NM4": "Názov kraja"})
data["Podiel platných hlasov v %"] = data["Podiel platných hlasov v %"].astype(str).str.replace(",", ".").astype(float)

# Získanie zoznamu politických subjektov 
subjekty = data["Názov politického subjektu"].unique()

def zobraz_mapu(subjekt):
    df_filtered = data[data["Názov politického subjektu"] == subjekt]
    geo_merged = geo_data.merge(df_filtered, on="Názov kraja", how="left")

    fig, ax = plt.subplots(1, 1, figsize=(6, 6))  
    geo_merged.plot(
        column="Podiel platných hlasov v %",
        ax=ax,
        legend=True,
        legend_kwds={'label': "Podpora subjektu v %", 'orientation': "horizontal"},
        cmap="coolwarm",
        edgecolor="black"
    )

    for _, row in geo_merged.iterrows():
        if not pd.isna(row["Podiel platných hlasov v %"]):
            ax.annotate(
                f"{row['Podiel platných hlasov v %']:.1f}%",
                xy=(row["geometry"].centroid.x, row["geometry"].centroid.y),
                xytext=(5, 5),
                textcoords="offset points",
                ha='center',
                fontsize=8,
                color="black"
            )

    plt.title(f"Podpora politického subjektu: {subjekt}", fontsize=12)  
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.read()).decode("utf-8")
    plt.close(fig)

    return f"data:image/png;base64,{encoded_image}"


# Načítanie dát
csv_path = "data/NRSR2023_SK_tab03d.csv"
data2 = pd.read_csv(csv_path)

# Získanie zoznamu subjektov
subjekty2 = data2["Názov politického subjektu"].unique()
data2 = data2[data2["Názov kraja"] != "Cudzina"]

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

# Funkcia na vytvorenie tabuliek s podporou pre každý kraj
def vytvor_tabulky(subjekt):
    df_filtered = data2[data2["Názov politického subjektu"] == subjekt]
    tabulky = []

    for kraj in sorted(df_filtered["Názov kraja"].unique()):
        df_kraj = df_filtered[df_filtered["Názov kraja"] == kraj]

        okresy_data = []
        for okres in sorted(df_kraj["Názov okresu"].unique()):
            df_okres = df_kraj[df_kraj["Názov okresu"] == okres]
            
            for _, row in df_okres.iterrows():
                okresy_data.append({
                    "Názov okresu": row["Názov okresu"],
                    "Podiel platných hlasov v %": row["Podiel platných hlasov v %"]
                })

        # Získanie správneho názvu krajov v genitíve
        kraj_genitive = genitive_names.get(kraj, kraj)  
        okresy_data.sort(key=lambda x: x["Podiel platných hlasov v %"], reverse=True)

        # Vytvorenie tabuľky pre každý kraj
        tabulka = dash_table.DataTable(
            id=f"tabulka_{kraj}",
            columns=[
                {"name": "Názov okresu", "id": "Názov okresu"},
                {"name": "Podiel platných hlasov (%)", "id": "Podiel platných hlasov v %"}
            ],
            data=okresy_data,
            style_table={'overflowX': 'auto', 'marginBottom': '20px'},
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

        kraj_nazov = f"Podpora v okresoch {kraj_genitive}"

        # Pridanie tabuľky do zoznamu tabuliek
        tabulky.append(
            html.Div([
                html.H4(kraj_nazov, style={
                    'textAlign': 'center',
                    'fontFamily': 'Roboto',
                    'color': 'black',
                    'fontSize': '24px',
                    'fontWeight': 'bold'
                }),
                tabulka
            ], style={"display": "inline-block", "width": "48%", "verticalAlign": "top", "marginBottom": "20px"})
        )
    
    # Vytvorenie layoutu 
    return html.Div(
        tabulky,
        style={
            "display": "flex",
            "flexWrap": "wrap",
            "justifyContent": "space-between",
            "gap": "20px"  
        }
    )

def get_layout():
    return html.Div([
        html.H2("Mapa podpory politických subjektov podľa krajov a okresov", style={
            'textAlign': 'center',
            'marginBottom': '40px',
            'marginTop': '20px',
            'fontFamily': 'Roboto',
            'color': 'black'
        }),

        html.Label("Vyberte subjekt:", style={
            "fontFamily": "Roboto",
            "fontSize": "18px",
            "fontStyle": "italic",
            "textAlign": "center",
            "display": "block",
            "marginBottom": "10px"
        }),

        dcc.Dropdown(
            id="subjekt-dropdown",
            options=[{"label": s, "value": s} for s in subjekty],
            value=subjekty[0],  # Default na prvý subjekt bez orezania
            style={
                "width": "60%",
                "margin": "0 auto",
                "fontFamily": "Roboto"
            }
        ),

        html.Img(id="mapa-obrazok", style={
            "width": "50%",
            "height": "auto",
            "marginTop": "30px",
            "display": "block",
            "marginLeft": "auto",
            "marginRight": "auto"
        }),
        html.Div(id="tabulky-kraje", style={"marginTop": "30px"})
    ], style={'padding': '20px'})
