import pandas as pd
import glob

# Cesta k priečinku s CSV súbormi
data_path = 'data/*.csv'

# Mapovanie pre premenovanie
rename_dict = {
    "OĽANO A PRIATELIA: OBYČAJNÍ ĽUDIA (OĽANO), NEZÁVISLÍ KANDIDÁTI (NEKA), NOVA, SLOBODNÍ A ZODPOVEDNÍ, PAČIVALE ROMA, MAGYAR SZÍVEK a Kresťanská únia a ZA ĽUDÍ": "OĽANO A PRIATELIA",
    "Maďarské fórum, Občianski demokrati Slovenska, Za regióny, Rómska koalícia, Demokratická strana": "Maďarské fórum",
    "SZÖVETSÉG - Magyarok. Nemzetiségek. Regiók. | ALIANCIA - Maďari. Národnosti. Regióny": "SZÖVETSÉG - Magyarok",
    "SRDCE vlastenci a dôchodcovia - SLOVENSKÁ NÁRODNÁ JEDNOTA": "SRDCE vlastenci a dôchodcovia",
    "SDKÚ - DS - Slovenská demokratická a kresťanská únia - Demokratická strana": "SDKU - DS"
}

# Prechádza všetky CSV súbory v priečinku
for file_path in glob.glob(data_path):
    df = pd.read_csv(file_path)
    if "Názov politického subjektu" in df.columns:
        df["Názov politického subjektu"] = df["Názov politického subjektu"].replace(rename_dict)

    df.to_csv(file_path, index=False)

print("Premenovanie dokončené.")
