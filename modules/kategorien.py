import streamlit as st
import plotly.express as px

# Optional: manuelle Übersetzungstabelle für primaryTopic
import streamlit as st
import plotly.express as px

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

        # Download-Button
        png = fig.to_image(format="png", width=800, height=400)
        st.download_button(
            "Download Themenverteilung (gesamt)",
            data=png,
            file_name="themenverteilung_gesamt.png",
            mime="image/png"
        )

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

    # Gruppieren und übersetzen
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

    png2 = fig2.to_image(format="png", width=900, height=450)
    st.download_button(
        "Download Themenvergleich nach Bezirk",
        data=png2,
        file_name="themen_vergleich_bezirk.png",
        mime="image/png"
    )


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

        # Download-Button
        png = fig.to_image(format="png", width=800, height=400)
        st.download_button(
            "Download Themenverteilung (gesamt)",
            data=png,
            file_name="themenverteilung_gesamt.png",
            mime="image/png"
        )

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

    # Gruppieren und übersetzen
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

    png2 = fig2.to_image(format="png", width=900, height=450)
    st.download_button(
        "Download Themenvergleich nach Bezirk",
        data=png2,
        file_name="themen_vergleich_bezirk.png",
        mime="image/png"
    )
