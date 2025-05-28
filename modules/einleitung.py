import streamlit as st
import plotly.express as px

def show_intro(df):
    st.title("🌐 Social Map Berlin Dashboard")
    st.markdown("""
    Willkommen im **Social Map Berlin Dashboard**!  
    Hier findest du eine **visuelle Übersicht** der aktuellen Einträge in der Social Map Berlin.  

    🔗 Die zugrundeliegenden Daten stammen aus der öffentlichen API:  
    [https://public.socialmap-berlin.de/items](https://public.socialmap-berlin.de/items)

    Das Dashboard bietet:
    - 📊 Eine Übersicht der Daten
    - ⏱️ Zeitliche Entwicklungen
    - 🗂️ Thematische Einblicke (z. B. nach Kategorien)
    - ✉️ Statistiken und Excel-Downloadmöglichkeiten zu E-Mail-Domains
    """)

    st.markdown("---")
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
            color_discrete_sequence=px.colors.qualitative.Set3,
            height=500,
            title="Verteilung der Einträge nach Bezirk"
        )
        fig_bzr.update_traces(textposition='outside')
        st.plotly_chart(fig_bzr, use_container_width=True)

    st.markdown("---")
    st.header("🏘️ Anzahl Einträge nach Berliner Stadtteilen in Bezirken")

    if bezirk_counts.empty:
        st.info("Bitte lade zuerst die Daten, um die Stadtteil-Übersicht anzuzeigen.")
    else:
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
                color_discrete_sequence=px.colors.qualitative.Set2,
                height=600,
                title=f"Verteilung der Einträge nach Stadtteil ({ausgewaehlter_bezirk})"
            )
            fig_st.update_traces(textposition='outside')
            st.plotly_chart(fig_st, use_container_width=True)
