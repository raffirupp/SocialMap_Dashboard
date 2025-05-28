import streamlit as st
import pandas as pd
from modules.fetch_data import load_items
from modules.einleitung import show_intro
from modules.fehlzuordnungen import show_unmatched
from modules.zeitliche_analyse import show_time_analysis
from modules.kategorien import show_category_plots
from modules.email_domains import show_email_domains
from modules.plz_mapping import load_mapping  # <- Import statt eigene Funktion

# Konfiguration
st.set_page_config(page_title="Paritätisches Dashboard", layout="wide")

# --- Daten laden ---
df = load_items()

# zip in str umwandeln, um Merge sicherzustellen
df['zip'] = df['zip'].astype(str).str.strip()

# Mapping laden
mapping = load_mapping('data/PLZ_Matching.xlsx')
mapping['PLZ'] = mapping['PLZ'].astype(str).str.strip()

# Merge auf PLZ → neue Spalten 'Bezirk' und 'Stadtteil'
df = df.merge(
    mapping[['PLZ', 'Bezirk', 'Stadtteil']],
    how='left', left_on='zip', right_on='PLZ'
)

# Umbenennen für bessere Lesbarkeit
df.rename(columns={'zip': 'Postleitzahl'}, inplace=True)

# --- Sidebar ---
menu = st.sidebar.radio(
    "Bereiche",
    [
        "Einleitung",
        "Datenübersicht",
        "Zeitliche Analyse",
        "Kategorien",
        "Email-Domains",
        "Unzugeordnete Einträge"  # <- NEU
    ]
)


# Dashboard-Rendering
def render_dashboard():
    if menu == "Einleitung":
        show_intro(df)

    elif menu == "Datenübersicht":
        st.header("📊 Datenübersicht")

        st.markdown("""
        In der folgenden Übersicht erhältst du einen ersten Einblick in den aktuellen Datenbestand der Social Map Berlin.

        Insgesamt sind derzeit **{:,} Einträge** in der Datenbank enthalten.  
        Jeder dieser Einträge beschreibt ein soziales Projekt, Angebot oder eine Einrichtung in Berlin oder Umgebung.

        Die Tabelle unten zeigt die Struktur des Datensatzes anhand von 10 Beispielen – also welche Spalten bzw. Variablen zur Verfügung stehen.  
        Diese Felder bilden die Grundlage für alle weiteren Auswertungen im Dashboard und diese können wir in der Zukunft gerne für euch auswerten.
        """.format(len(df)))

        st.subheader("🔍 Beispielhafte Datensätze")
        st.dataframe(df.head(10))

        st.markdown("---")
        st.subheader("📌 Informationen zur Postleitzahl-Zuordnung")

        st.markdown("""
        Insgesamt enthalten **{:,} Einträge eine Postleitzahl**.  
        Davon konnten **{:,} eindeutig einem Berliner Bezirk** zugeordnet werden.

        Auch **{:,} Einträge** konnten zusätzlich einem Stadtteil zugewiesen werden.  
        Die Domain (z. B. für Mailkontakt) ist bei **{:,} Einträgen** verfügbar. 

        In Einzelfällen fehlen diese Zuordnungen, z. B. weil die PLZ nicht im Berliner Raum liegt  
        oder ein **Tippfehler** vorliegt. Diese werden im Abschnitt **„Unzugeordnete Einträge“** separat aufgeführt. 
        """.format(
            df['Postleitzahl'].notna().sum(),
            df['Bezirk'].notna().sum(),
            df['Stadtteil'].notna().sum(),
            df['domain'].notna().sum() if 'domain' in df.columns else 0
        ))
        st.markdown("### 📋 Alle vorkommenden Kategorien`")

        if "primaryTopic" in df.columns:
            unique_topics = df["primaryTopic"].dropna().unique()
            st.write(f"Insgesamt **{len(unique_topics)} unterschiedliche Werte**, die als Grundlage für die Kategorien-Auswertung dienen und wieder auf deutsch übersetzt wurden`:")
            st.write(sorted(unique_topics))
        else:
            st.warning("Spalte `primaryTopic` nicht vorhanden.")


    elif menu == "Zeitliche Analyse":
        show_time_analysis(df)

    elif menu == "Kategorien":
        show_category_plots(df)

    elif menu == "Email-Domains":
        st.header("✉️ Email-Domain-Analyse nach Bezirk/Stadtteil")
        bezirke = ['Alle'] + sorted(df['Bezirk'].dropna().unique().tolist())
        sel_b = st.selectbox("Bezirk wählen:", bezirke)
        if sel_b != 'Alle':
            df_b = df[df['Bezirk'] == sel_b]
            st.write(f"**Auswahl Bezirk:** {sel_b}")
            st.subheader("Stadtteil wählen")
            stadtteile = ['Alle'] + sorted(df_b['Stadtteil'].dropna().unique().tolist())
            sel_s = st.selectbox("Stadtteil wählen:", stadtteile)
            if sel_s != 'Alle':
                sub_df = df_b[df_b['Stadtteil'] == sel_s]
                st.write(f"**Auswahl Stadtteil:** {sel_s}")
            else:
                sub_df = df_b
        else:
            sub_df = df
        show_email_domains(sub_df)

    elif menu == "Unzugeordnete Einträge":
        show_unmatched(df)

render_dashboard()
