import streamlit as st
import plotly.express as px

def show_time_analysis(df):
    st.header("⏱️ Zeitliche Analyse")

    # --- 1. Übersicht ganz Berlin ---
    st.subheader("🔍 Gesamtübersicht aller Einträge (Berlin-weit)")

    if "lastEditDate" in df.columns:
        fig_gesamt = px.histogram(
            df, x="lastEditDate", nbins=30,
            title="Verteilung der letzten Änderungsdaten (Berlin gesamt)"
        )
        fig_gesamt.update_layout(
            xaxis_title="Datum",
            yaxis_title="Anzahl Einträge",
            bargap=0.1
        )
        st.plotly_chart(fig_gesamt, use_container_width=True)

    # --- 2. Bezirksvergleich ---
    st.markdown("---")
    st.subheader("📊 Bezirksvergleich (Mehrfachauswahl)")

    bezirke = sorted(df['Bezirk'].dropna().unique())
    default_bezirke = ['Mitte-Wedding-Tiergarten', 'Friedrichshain-Kreuzberg']  # <-- anpassbar

    ausgewaehlte_bezirke = st.multiselect(
        "Bezirke auswählen (Standard: Mitte & Friedrichshain):",
        options=bezirke,
        default=[b for b in default_bezirke if b in bezirke]
    )

    df_filtered = df[df['Bezirk'].isin(ausgewaehlte_bezirke)]

    if df_filtered.empty:
        st.warning("Keine Einträge für die ausgewählten Bezirke.")
    else:
        fig_vergleich = px.histogram(
            df_filtered, x="lastEditDate", nbins=30,
            color="Bezirk",
            title="Letzte Änderungen nach Bezirk (Vergleich)"
        )
        fig_vergleich.update_layout(
            xaxis_title="Datum",
            yaxis_title="Anzahl Einträge",
            bargap=0.1
        )
        st.plotly_chart(fig_vergleich, use_container_width=True)
