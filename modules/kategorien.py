import streamlit as st
import plotly.express as px
import pandas as pd
from io import BytesIO

# Optional: manuelle Übersetzungstabelle für primaryTopic
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


def show_category_plots(df):
    st.header("🗂️ Thematische Verteilung (primaryTopic)")

    # 🔹 1. Gesamtauswertung: Balkendiagramm auf Deutsch
    if "primaryTopic" in df.columns:
        topic_counts = df["primaryTopic"].value_counts().reset_index()
        topic_counts.columns = ["primaryTopic", "topic_count"]

        # Kategorien übersetzen
        topic_counts["primaryTopic_de"] = topic_counts["primaryTopic"].map(topic_translation).fillna(topic_counts["primaryTopic"])

        fig = px.bar(
            topic_counts,
            x="primaryTopic_de",
            y="topic_count",
            text="topic_count",
            title="Thematische Verteilung aller Einträge (gesamt)"
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(xaxis_tickangle=-45, xaxis_title="Thema", yaxis_title="Anzahl Einträge")

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Spalte `primaryTopic` nicht vorhanden.")

    # 🔹 2. Nach Bezirk filtern
    st.markdown("---")
    st.subheader("📍 Thematische Verteilung nach Bezirk")

    bezirke = sorted(df['Bezirk'].dropna().unique())
    default_bezirke = ["Mitte-Wedding-Tiergarten", "Neukölln", "Pankow-Prenzlauer Berg-Weißensee"]

    ausgewaehlte_bezirke = st.multiselect(
        "Bezirk(e) auswählen:",
        options=bezirke,
        default=[b for b in default_bezirke if b in bezirke]
    )

    df_filtered = df[df['Bezirk'].isin(ausgewaehlte_bezirke)]

    if df_filtered.empty:
        st.info("Keine Einträge für die ausgewählten Bezirke vorhanden.")
        return

    grouped = df_filtered.groupby(["Bezirk", "primaryTopic"]).size().reset_index(name="Anzahl")
    grouped["Thema"] = grouped["primaryTopic"].map(topic_translation).fillna(grouped["primaryTopic"])

    fig2 = px.bar(
        grouped,
        x="Thema",
        y="Anzahl",
        color="Bezirk",
        barmode="group",
        title="Themen nach ausgewählten Bezirken"
    )
    fig2.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig2, use_container_width=True)

    # ----------------------------------------------------
    # 🏠 Art der Einrichtung (Filter + Excel-Export)
    # ----------------------------------------------------
    st.markdown("---")
    st.subheader("🏠 Art der Einrichtung – Detailauswertung & Download")

    if "primaryTopic" not in df.columns:
        st.warning("Spalte 'primaryTopic' nicht vorhanden – keine Auswertung möglich.")
        return

    # 🔹 Englische & deutsche Bezeichnungen kombinieren
    einrichtungsarten = sorted(df["primaryTopic"].dropna().unique().tolist())
    einrichtungsarten_de = [
        topic_translation.get(t, t) for t in einrichtungsarten
    ]
    # Mapping Deutsch → Englisch, damit Filter funktioniert
    reverse_translation = {v: k for k, v in topic_translation.items()}

    # Auswahlfeld mit deutscher Anzeige
    art_sel_de = st.selectbox(
        "Art der Einrichtung auswählen:",
        options=einrichtungsarten_de,
        help="Basierend auf dem Feld 'primaryTopic'."
    )

    # Intern auf englischen Schlüssel zurückübersetzen
    art_sel = reverse_translation.get(art_sel_de, art_sel_de)

    # 🔹 Auswahlfelder für Bezirk & Organisation
    col1, col2 = st.columns(2)
    with col1:
        bezirk_sel = st.selectbox(
            "Bezirk auswählen:",
            options=["Alle"] + sorted(df["Bezirk"].dropna().unique())
        )
    with col2:
        org_sel = st.selectbox(
            "Mitgliedsorganisation auswählen:",
            options=["Alle"] + sorted(df["Organisation"].dropna().unique())
        )

    # 🔹 Filter anwenden
    df_filtered = df[df["primaryTopic"] == art_sel]
    if bezirk_sel != "Alle":
        df_filtered = df_filtered[df_filtered["Bezirk"] == bezirk_sel]
    if org_sel != "Alle":
        df_filtered = df_filtered[df_filtered["Organisation"] == org_sel]

    if df_filtered.empty:
        st.info("Keine Einträge für diese Auswahl vorhanden.")
        return

    # 🔹 Themenbezeichnung übersetzen
    df_filtered["Thema"] = df_filtered["primaryTopic"].map(topic_translation).fillna(df_filtered["primaryTopic"])

    # 🔹 Tabelle anzeigen
    st.dataframe(df_filtered[["title", "Organisation", "Bezirk", "Stadtteil", "Thema", "email"]])

    # 🔹 Excel-Download
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_filtered.to_excel(writer, index=False, sheet_name="Einrichtungen")
    excel_data = output.getvalue()

    st.download_button(
        label="📥 Download als Excel-Datei",
        data=excel_data,
        file_name=f"einrichtungen_{art_sel}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )