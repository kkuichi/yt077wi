# Generovanie štatistík a vizualizácií z kandidátskych listín do volieb

---

## Úvod

Tento projekt sa venuje analýze a vizualizácii volebných dát zo Slovenskej republiky, konkrétne z kandidátskych listín do Národnej rady SR v roku 2023.  

Cieľom je vytvoriť **prehľadné a interaktívne vizualizácie** štatistík o preferenčných hlasoch kandidátov, výsledkoch politických strán a ďalších dôležitých ukazovateľoch.

Výstupy projektu sú určené pre **výskumníkov a verejnosť** so záujmom o detailné analýzy volebných výsledkov a demografických údajov kandidátov.

Projekt obsahuje **webovú aplikáciu**, ktorá umožňuje jednoducho prehliadať tieto štatistiky.

---

## Ciele projektu

- Načítať a predspracovať dáta z kandidátskych listín a volebných výsledkov v rôznych úrovniach (SR, kraj, okres)
- Vytvoriť prehľadné vizualizácie preferenčných hlasov, počtu kandidátov, úspešnosti politických subjektov a ďalších metrík
- Poskytnúť možnosť **interaktívnej navigácie** medzi rôznymi úrovňami geografických a politických štatistík
- Zabezpečiť prehľadné a zrozumiteľné zobrazenie dát vhodné pre ďalšiu analýzu a prezentáciu
- Podporiť **transparentnosť a dostupnosť informácií o voľbách** pre širokú verejnosť

---

## Ukážka výstupu

- Charakteristiky kandidátov Národnej rady SR 2023  
- Volebná účasť na Slovensku (kraje a okresy)  
- Mapa podpory politických subjektov podľa krajov a okresov  
- Analýza výsledkov politických subjektov a kandidátov  
- Preferencie politických subjektov a víťazi podľa krajov  
- Analýza mandátov a hlasovania  

---

## Webová aplikácia

Aplikácia je dostupná online na adrese:  
👉 [https://bp-xf8c.onrender.com](https://bp-xf8c.onrender.com)

---

## Použité technológie a knižnice

- **Python 3.9+**
- `pandas` – spracovanie dát
- `geopandas` – práca s geografickými dátami
- `plotly.express`, `plotly.graph_objects` – interaktívne vizualizácie
- `matplotlib` – statické vizualizácie vrátane `patches` a `colors`
- `seaborn` – pokročilé vizualizácie a štatistické grafy
- `ipywidgets` – interaktívne widgety pre Jupyter Notebook
- `dash`, `dash_bootstrap_components` – tvorba webovej aplikácie
- `dash.exceptions.PreventUpdate` – ovládanie aktualizácií v Dash aplikácii
- `dash_table` – tvorba a správa tabuliek v Dash aplikácii
- `io`, `base64` – spracovanie a kódovanie dát (napríklad obrázky)
- `glob` – správa súborov a cesta k súborom
