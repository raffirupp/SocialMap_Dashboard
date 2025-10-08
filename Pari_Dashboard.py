# Pari_Dashboard.py

import streamlit as st
import pandas as pd
from modules.fetch_data import load_items
from modules.einleitung import show_intro
from modules.organisationen import show_organisationen
from modules.fehlzuordnungen import show_unmatched
from modules.zeitliche_analyse import show_time_analysis
from modules.kategorien import show_category_plots
from modules.email_domains import show_email_domains
from modules.plz_mapping import load_mapping

import plotly.io as pio

# ----------------------------------
# Plotly Theme: Paritätisches Corporate Design
# ----------------------------------
pio.templates.default = "plotly_white"
pio.templates["plotly_white"].layout.font.family = "Atkinson Hyperlegible, Arial, sans-serif"
pio.templates["plotly_white"].layout.font.color = "#333333"
pio.templates["plotly_white"].layout.title.font.family = "Atkinson Hyperlegible, Arial, sans-serif"
pio.templates["plotly_white"].layout.title.font.color = "#0063A6"

# ----------------------------------
# Streamlit-Seitenkonfiguration
# ----------------------------------
st.set_page_config(
    page_title="Social Map Berlin Dashboard",
    layout="wide",
    page_icon="🌍"
)

# ----------------------------------
# Schriftart & Grundlayout (CSS)
# ----------------------------------
st.markdown(
    """
    <style>
    @font-face {
        font-family: 'Atkinson Hyperlegible';
        font-style: normal;
        font-weight: 400;
        src: url('https://fonts.gstatic.com/s/atkinsonhyperlegible/v15/memXYaGpT0IYG-gTq5LzWx_Ux4WZV2P3V0E.woff2') format('woff2');
    }

    html, body, [class*="css"] {
        font-family: 'Atkinson Hyperlegible', Arial, sans-serif !important;
        color: #333333;
        line-height: 1.6;
    }

    h1, h2, h3, h4 {
        font-family: 'Atkinson Hyperlegible', Arial, sans-serif !important;
        color: #0063A6 !important;
        font-weight: 700 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------------
# Daten laden (Items + Organisationen)
# ----------------------------------
df, data_source = load_items()
st.sidebar.info(f"💾 Datenquelle: {data_source.upper()}")

if "zip" not in df.columns:
    st.warning("⚠️ Es wurden keine Postleitzahlen aus der API geladen. Das Dashboard ist daher möglicherweise unvollständig.")
    df["zip"] = None

df["zip"] = df["zip"].astype(str).str.strip()

# ----------------------------------
# PLZ-zu-Sozialraum-Mapping laden und zusammenführen
# ----------------------------------
mapping = load_mapping("data/berlin_plz_to_sozialraum.xlsx")

if not mapping.empty:
    mapping["PLZ"] = mapping["PLZ"].astype(str).str.strip()
    merge_cols = ["PLZ", "Bezirk", "Stadtteil"]

    for extra in ["Bezirksregion_Name", "Prognoseraum_Name", "Planungsraum_Name"]:
        if extra in mapping.columns:
            merge_cols.append(extra)

    df = df.merge(mapping[merge_cols], how="left", left_on="zip", right_on="PLZ")
    df.rename(columns={"zip": "Postleitzahl"}, inplace=True)
    #print(f"✅ PLZ-Mapping erfolgreich verknüpft: {df['Bezirk'].notna().sum()} / {len(df)} Einträge")
else:
    st.error("⚠️ Das PLZ-Sozialraum-Mapping konnte nicht geladen werden. Bitte Datei prüfen.")
    df["Bezirk"] = None
    df["Stadtteil"] = None

# ----------------------------------
# Sidebar-Menü
# ----------------------------------
menu = st.sidebar.selectbox(
    "🔎 Wähle einen Bereich:",
    [
        "Einleitung",
        "Mitgliedsorganisationen",
        "Kategorien",
        "Email-Domains",
        "Unzugeordnete Einträge",
        "Datenübersicht",
        "Archiv"
    ],
    index=0
)

# ----------------------------------
# Haupt-Dashboard-Rendering
# ----------------------------------
def render_dashboard():
    if menu == "Einleitung":
        show_intro(df)

    elif menu == "Mitgliedsorganisationen":
        show_organisationen(df)

    elif menu == "Kategorien":
        show_category_plots(df)

    elif menu == "Email-Domains":
        st.header("✉️ Email-Domain-Analyse nach Bezirk")
        bezirke = ["Alle"] + sorted(df["Bezirk"].dropna().unique().tolist())
        selected_bezirk = st.selectbox("Bezirk auswählen:", bezirke)
        sub_df = df if selected_bezirk == "Alle" else df[df["Bezirk"] == selected_bezirk]
        show_email_domains(sub_df)

    elif menu == "Unzugeordnete Einträge":
        show_unmatched(df)

    elif menu == "Datenübersicht":
        st.header("📊 Datenübersicht")

        st.markdown(f"""
        Dieses Dashboard enthält aktuell **{len(df):,} Einträge**.  
        Jeder Eintrag beschreibt ein soziales Projekt, Angebot oder eine Einrichtung in Berlin oder Umgebung.
        """)

        st.subheader("📋 Beispielhafte Datensätze")
        st.dataframe(df.head(10))

        st.markdown("---")
        st.subheader("📌 Postleitzahlen- und Raumzuordnung")

        n_plz = df["Postleitzahl"].notna().sum() if "Postleitzahl" in df.columns else 0
        n_bezirk = df["Bezirk"].notna().sum() if "Bezirk" in df.columns else 0
        n_stadtteil = df["Stadtteil"].notna().sum() if "Stadtteil" in df.columns else 0
        n_org = df["Organisation"].notna().sum() if "Organisation" in df.columns else 0

        sozialraum_spalten = ["Planungsraum_Name", "Bezirksregion_Name", "Prognoseraum_Name"]
        sozialraum_counts = {ebene: df[ebene].notna().sum() for ebene in sozialraum_spalten if ebene in df.columns}

        st.markdown(f"""
        - **{n_plz:,} Einträge** enthalten eine Postleitzahl  
        - **{n_bezirk:,} Einträge** konnten einem Berliner **Bezirk** zugeordnet werden  
        - **{n_stadtteil:,} Einträge** enthalten eine **Stadtteil**-Zuordnung  
        - **{n_org:,} Einträge** sind einer **Mitgliedsorganisation** zugeordnet
        """)

        if sozialraum_counts:
            st.markdown("#### 🔹 Zuordnung zu Sozialräumen")
            for ebene, anz in sozialraum_counts.items():
                st.markdown(f"- **{anz:,} Einträge** enthalten eine Zuordnung zur Ebene *{ebene.replace('_Name','')}*")
        else:
            st.info("Keine Zuordnungen zu Sozialräumen gefunden.")

        st.markdown("---")
        st.subheader("🗂️ Themenkategorien (deutsch)")

        topic_translation = {
            "housing": "Wohnen",
            "counseling": "Beratung",
            "kindergarden": "Kindergarten",
            "neighborhood": "Nachbarschaft",
            "recreation": "Freizeit",
            "self_help": "Selbsthilfe",
            "education": "Bildung",
            "labour": "Arbeit",
            "addiction": "Sucht",
            "care": "Pflege",
            "health": "Gesundheit",
            "volunteer_work": "Ehrenamt",
            "sports": "Sport",
            "arts": "Kunst",
            "hospice": "Hospiz",
            "victim_support": "Opferhilfe",
            "offender_services": "Täterarbeit",
            "lobby": "Interessenvertretung",
            "encounters": "Begegnung"
        }

        if "primaryTopic" in df.columns:
            unique_topics = sorted(df["primaryTopic"].dropna().unique())
            translated = [topic_translation.get(t, t) for t in unique_topics]
            st.write(f"Insgesamt gibt es **{len(translated)} unterschiedliche Themenbereiche:**")
            st.write(", ".join(translated))
        else:
            st.warning("Die Spalte `primaryTopic` ist nicht verfügbar.")

    elif menu == "Archiv":
        show_time_analysis(df)

# ----------------------------------
# Dashboard starten
# ----------------------------------
render_dashboard()
