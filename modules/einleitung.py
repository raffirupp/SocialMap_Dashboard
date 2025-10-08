# modules/einleitung.py
import streamlit as st
import plotly.express as px
import pandas as pd

def show_intro(df):
    # ----------------------------------
    # Titel & Einführung
    # ----------------------------------
    st.title("🌐 Social Map Berlin Dashboard")

    st.markdown("""
    Willkommen im **Social Map Berlin Dashboard**!  
    Hier findest du eine **visuelle Übersicht** über die Angebote, Projekte und Mitgliedsorganisationen
    des Paritätischen Wohlfahrtsverbands in Berlin – basierend auf den Daten der Social Map Berlin.

    🔗 **Datenquellen:**
    - [https://public.socialmap-berlin.de/items](https://public.socialmap-berlin.de/items) → Basisdaten zu Angeboten und Projekten  
    - [https://api.socialmap-berlin.de/options](https://api.socialmap-berlin.de/options) → Zuordnung zu Mitgliedsorganisationen  
    - [https://gdi.berlin.de/services/wfs/lor_2021](https://gdi.berlin.de/services/wfs/lor_2021) → Offizielle Sozialraumdaten (LOR: Planungsräume, Bezirksregionen, Prognoseräume)
    """)

    # ----------------------------------
    # Neue Funktionen und Updates
    # ----------------------------------
    st.info("""
    ### 🆕 Was ist neu im Dashboard?

    Seit dem letzten Update wurden mehrere Erweiterungen und Verbesserungen umgesetzt:

    - 🕒 **Zeitliche Analyse** wurde in den Reiter *Archiv* verschoben  
      → dort lassen sich historische Entwicklungen gezielt auswerten.

    - 🧭 **Verknüpfung mit den Berliner Sozialräumen (LOR-System)**  
      → Einträge können jetzt den Ebenen *Planungsraum*, *Bezirksregion* und *Prognoseraum* zugeordnet werden.

    - 🏢 **Neue Auswertungen nach Mitgliedsorganisationen**  
      → Auswahl mehrerer Organisationen gleichzeitig, inklusive Detail- und Download-Optionen.

    - 🗂️ **Erneuerter Reiter „Kategorien“**  
      → Alle Themen erscheinen jetzt auf Deutsch, ergänzt um Filter- und Exportfunktionen.

    - 📥 **Erweiterte Downloadmöglichkeiten**  
      → Exporte sind nun flexibel nach Organisation, Bezirk oder Themengebiet möglich.

    - 🎨 **Corporate Design des Paritätischen Berlin**  
      → Einheitliche Farben (#0063A6 / #CC051C) und barrierearme Darstellung.

    Bei Fragen oder Verbesserungsvorschlägen meldet euch sehr gerne.
    """)

    st.markdown("""
    ---
    **Das Dashboard bietet:**
    - 📊 Eine Übersicht der Daten  
    - 🧩 Auswertung nach Mitgliedsorganisationen  
    - 🗂️ Thematische Einblicke (z. B. nach Kategorien)  
    - ✉️ Statistiken und Excel-Downloadmöglichkeiten zu E-Mail-Domains
    """)

    st.markdown("---")

    # ----------------------------------
    # Bezirksebene
    # ----------------------------------
    st.header("🏙️ Anzahl Einträge nach Berliner Bezirken")

    bezirk_counts = df['Bezirk'].value_counts().reset_index()
    bezirk_counts.columns = ['Bezirk', 'Anzahl']

    if bezirk_counts.empty:
        st.warning("⚠️ Keine Bezirk-Daten verfügbar.")
    else:
        fig_bzr = px.bar(
            bezirk_counts,
            x='Anzahl',
            y='Bezirk',
            orientation='h',
            color='Bezirk',
            text='Anzahl',
            color_discrete_sequence=["#0063A6"],
            height=500,
            title="Verteilung der Einträge nach Bezirk"
        )
        fig_bzr.update_traces(textposition='outside')
        fig_bzr.update_layout(showlegend=False)
        st.plotly_chart(fig_bzr, use_container_width=True)

    # ----------------------------------
    # Stadtteile innerhalb eines Bezirks
    # ----------------------------------
    st.markdown("---")
    st.header("🏘️ Anzahl Einträge nach Berliner Stadtteilen in Bezirken")

    if bezirk_counts.empty:
        st.info("Bitte lade zuerst die Daten, um die Stadtteil-Übersicht anzuzeigen.")
        return

    ausgewaehlter_bezirk = st.selectbox(
        "Wähle einen Bezirk aus:",
        sorted(df['Bezirk'].dropna().unique())
    )
    df_filtered = df[df['Bezirk'] == ausgewaehlter_bezirk]
    stadt_counts = df_filtered['Stadtteil'].value_counts().reset_index()
    stadt_counts.columns = ['Stadtteil', 'Anzahl']

    if stadt_counts.empty:
        st.info(f"Keine Einträge für {ausgewaehlter_bezirk} vorhanden.")
    else:
        fig_st = px.bar(
            stadt_counts,
            x='Anzahl',
            y='Stadtteil',
            orientation='h',
            color='Stadtteil',
            text='Anzahl',
            color_discrete_sequence=["#0099C6", "#0063A6", "#CC051C"],
            height=600,
            title=f"Verteilung der Einträge nach Stadtteil ({ausgewaehlter_bezirk})"
        )
        fig_st.update_traces(textposition='outside')
        fig_st.update_layout(showlegend=False)
        st.plotly_chart(fig_st, use_container_width=True)

    # ----------------------------------
    # Neue Sektion: Sozialraum-Analyse
    # ----------------------------------
    st.markdown("---")
    st.header("🧭 Verteilung nach Sozialräumen")

    # Prüfen, ob Sozialraumspalten existieren
    sozialraum_spalten = [
        'Planungsraum_Name',
        'Bezirksregion_Name',
        'Prognoseraum_Name'
    ]
    vorhandene = [s for s in sozialraum_spalten if s in df.columns]

    if not vorhandene:
        st.info("⚠️ Keine Sozialraum-Daten vorhanden. Bitte Mapping-Datei prüfen.")
        return

    # Auswahl der Ebene
    ausgewaehlte_ebene = st.selectbox(
        "Wähle die Ebene des Sozialraums:",
        vorhandene,
        format_func=lambda x: x.replace("_Name", "").replace("_", " ")
    )

    df_sozial = df[df['Bezirk'] == ausgewaehlter_bezirk]
    counts_sozial = df_sozial[ausgewaehlte_ebene].value_counts().reset_index()
    counts_sozial.columns = [ausgewaehlte_ebene, 'Anzahl']

    if counts_sozial.empty:
        st.info(f"Keine Einträge für {ausgewaehlter_bezirk} auf Ebene {ausgewaehlte_ebene}.")
    else:
        fig_soz = px.bar(
            counts_sozial,
            x='Anzahl',
            y=ausgewaehlte_ebene,
            orientation='h',
            color=ausgewaehlte_ebene,
            text='Anzahl',
            color_discrete_sequence=["#0063A6"],
            height=600,
            title=f"Verteilung nach Sozialräumen in {ausgewaehlter_bezirk} ({ausgewaehlte_ebene.replace('_Name','')})"
        )
        fig_soz.update_traces(textposition='outside')
        fig_soz.update_layout(showlegend=False)
        st.plotly_chart(fig_soz, use_container_width=True)
