import streamlit as st
import pandas as pd
from modules.fetch_data import load_items
from modules.einleitung import show_intro
from modules.fehlzuordnungen import show_unmatched
from modules.zeitliche_analyse import show_time_analysis
from modules.kategorien import show_category_plots
from modules.email_domains import show_email_domains
from modules.plz_mapping import load_mapping

# Streamlit-Seitenkonfiguration
st.set_page_config(
    page_title="Social Map Berlin Dashboard", 
    layout="wide", 
    page_icon="🌍"
)

# Daten laden
df = load_items()
if 'zip' not in df.columns:
    st.warning("⚠️ Es wurden keine Postleitzahlen aus der API geladen. Das Dashboard ist daher möglicherweise unvollständig.")
    df['zip'] = None

df['zip'] = df['zip'].astype(str).str.strip()

# Postleitzahl-Mapping laden und mit Daten verbinden
mapping = load_mapping('data/PLZ_Matching.xlsx')
mapping['PLZ'] = mapping['PLZ'].astype(str).str.strip()
df = df.merge(mapping[['PLZ', 'Bezirk', 'Stadtteil']], how='left', left_on='zip', right_on='PLZ')
df.rename(columns={'zip': 'Postleitzahl'}, inplace=True)

# Sidebar (mit besserer Benutzerführung)
menu = st.sidebar.selectbox(
    "🔎 Wähle einen Bereich:",
    [
        "Einleitung",
        "Datenübersicht",
        "Zeitliche Analyse",
        "Kategorien",
        "Email-Domains",
        "Unzugeordnete Einträge"
    ]
)

# Haupt-Dashboard-Rendering
def render_dashboard():
    if menu == "Einleitung":
        show_intro(df)

    elif menu == "Datenübersicht":
        st.header("📊 Datenübersicht")

        st.markdown(f"""
        Dieses Dashboard enthält aktuell **{len(df):,} Einträge**.  
        Jeder Eintrag beschreibt ein soziales Projekt, Angebot oder eine Einrichtung in Berlin oder Umgebung.

        Die Tabelle unten zeigt **10 Beispieleinträge**, damit du siehst, welche Informationen im Datensatz enthalten sind.  
        Diese Informationen bilden die Grundlage für alle weiteren Auswertungen im Dashboard.
        """)
        st.subheader("📋 Beispielhafte Datensätze")
        st.dataframe(df.head(10))

        st.markdown("---")
        st.subheader("📌 Postleitzahlen und Zuordnung")

        st.markdown(f"""
        - **{df['Postleitzahl'].notna().sum():,} Einträge** enthalten eine Postleitzahl.  
        - Davon konnten **{df['Bezirk'].notna().sum():,} Einträge** einem Berliner Bezirk zugeordnet werden.  
        - **{df['Stadtteil'].notna().sum():,} Einträge** enthalten eine Stadtteil-Zuordnung.  
        - Es sind **{df['domain'].notna().sum() if 'domain' in df.columns else 0:,} Einträge** mit einer E-Mail-Domain verfügbar.

        In manchen Fällen fehlen diese Angaben, zum Beispiel bei fehlerhaften Postleitzahlen oder weil die Daten außerhalb von Berlin liegen.  
        Diese werden im Abschnitt **„Unzugeordnete Einträge“** aufgeführt.
        """)
        st.markdown("### 🗂️ Alle vorkommenden Kategorien")
        if "primaryTopic" in df.columns:
            unique_topics = df["primaryTopic"].dropna().unique()
            st.write(f"Insgesamt gibt es **{len(unique_topics)} unterschiedliche Kategorien**, die für die Auswertung genutzt werden:")
            st.write(sorted(unique_topics))
        else:
            st.warning("Die Spalte `primaryTopic` ist nicht verfügbar.")

    elif menu == "Zeitliche Analyse":
        show_time_analysis(df)

    elif menu == "Kategorien":
        show_category_plots(df)

    elif menu == "Email-Domains":
        st.header("✉️ Email-Domain-Analyse nach Bezirk")
        bezirke = ['Alle'] + sorted(df['Bezirk'].dropna().unique().tolist())
        selected_bezirk = st.selectbox("Bezirk auswählen:", bezirke)
        sub_df = df if selected_bezirk == 'Alle' else df[df['Bezirk'] == selected_bezirk]
        show_email_domains(sub_df)

    elif menu == "Unzugeordnete Einträge":
        show_unmatched(df)

render_dashboard()
