import streamlit as st
import plotly.express as px

def show_intro(df):
    st.title("🌐 Social Map Berlin Dashboard")
    st.markdown("""
    Dieses Dashboard visualisiert und analysiert die aktuellen Einträge von
    Social Map Berlin direkt aus der API unter  
    https://public.socialmap-berlin.de/items  
    Es enthält:
    - Eine Datenübersicht  
    - Zeitliche Analysen  
    - Kategorische Verteilungen  
    - Email-Domain-Statistiken  
    """)

    st.markdown("---")
    st.header("🏙️ Verteilung nach Bezirk")

    bezirk_counts = df['Bezirk'].value_counts().reset_index()
    bezirk_counts.columns = ['Bezirk', 'Anzahl']

    fig_bzr = px.bar(
        bezirk_counts,
        x='Anzahl',
        y='Bezirk',
        orientation='h',
        color='Bezirk',
        text='Anzahl',  # <--- Beschriftung hinzugefügt
        color_discrete_sequence=px.colors.qualitative.Set3,
        height=500,
        title="Einträge pro Bezirk"
    )
    fig_bzr.update_traces(textposition='outside')  # <--- Position der Zahlen
    st.plotly_chart(fig_bzr, use_container_width=True)

    st.markdown("---")
    st.header("🏘️ Verteilung nach Stadtteil")

    # Dropdown für Bezirksauswahl
    ausgewaehlter_bezirk = st.selectbox(
        "Bezirk auswählen:", 
        sorted(df['Bezirk'].dropna().unique().tolist())
    )

    df_filtered = df[df['Bezirk'] == ausgewaehlter_bezirk]

    stadt_counts = df_filtered['Stadtteil'].value_counts().reset_index()
    stadt_counts.columns = ['Stadtteil', 'Anzahl']

    if stadt_counts.empty:
        st.info("Keine Einträge für diesen Bezirk vorhanden.")
    else:
        fig_st = px.bar(
            stadt_counts,
            x='Anzahl',
            y='Stadtteil',
            orientation='h',
            color='Stadtteil',
            text='Anzahl',  # <--- Beschriftung hinzugefügt
            color_discrete_sequence=px.colors.qualitative.Set2,
            height=600,
            title=f"Einträge nach Stadtteil in {ausgewaehlter_bezirk}"
        )
        fig_st.update_traces(textposition='outside')  # <--- Position der Zahlen
        st.plotly_chart(fig_st, use_container_width=True)
