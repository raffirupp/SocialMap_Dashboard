# modules/organisationen.py
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from modules.fetch_data import load_options


def show_organisationen(df: pd.DataFrame):
    st.title("🏢 Mitgliedsorganisationen")

    if "Organisation" not in df.columns:
        st.error("❌ Spalte 'Organisation' fehlt im Datensatz.")
        return

    # -------------------------------------------------------
    # 📥 Download-Bereich – immer sichtbar, unabhängig von Auswahl
    # -------------------------------------------------------
    st.subheader("📥 Download-Mitgliedsorganisationen")

    df_options = load_options()
    orgs_all = set(df_options["title"].dropna().unique()) if not df_options.empty else set()
    orgs_with_entries = set(df["Organisation"].dropna().unique())
    orgs_without_entries = orgs_all - orgs_with_entries

    auswahl = st.radio(
        "Welche Organisationen möchtest du exportieren?",
        [
            "Alle Organisationen mit Eintrag",
            "Alle Organisationen ohne Eintrag",
            "Nach Bezirk (nur Organisationen mit Eintrag)"
        ],
        index=0
    )

    if auswahl == "Alle Organisationen mit Eintrag":
        df_export = df[["Organisation", "Bezirk", "Stadtteil", "title"]].dropna(subset=["Organisation"]).drop_duplicates()

    elif auswahl == "Alle Organisationen ohne Eintrag":
        df_export = pd.DataFrame(sorted(orgs_without_entries), columns=["Organisation"])
        df_export["Bezirk"] = None
        df_export["Stadtteil"] = None
        df_export["title"] = None

    else:  # Nach Bezirk
        bezirk_sel = st.selectbox(
            "Bezirk auswählen:",
            sorted(df["Bezirk"].dropna().unique())
        )
        df_export = (
            df[df["Bezirk"] == bezirk_sel][["Organisation", "Bezirk", "Stadtteil", "title"]]
            .dropna(subset=["Organisation"])
            .drop_duplicates()
        )

    if not df_export.empty:
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_export.to_excel(writer, index=False, sheet_name="Organisationen")
        excel_data = output.getvalue()

        st.download_button(
            label="📥 Download als Excel-Datei",
            data=excel_data,
            file_name="organisationen_export.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("Keine Organisationen für diese Auswahl gefunden.")

    st.markdown("---")

    # -------------------------------------------------------
    # 🔢 Überblick: Kennzahlen
    # -------------------------------------------------------
    st.subheader("📊 Überblick über die Mitgliedsorganisationen")

    total_entries = len(df)
    orgs_with_entries_count = df["Organisation"].dropna().nunique()
    entries_with_org = df["Organisation"].notna().sum()
    total_orgs_in_system = len(df_options) if not df_options.empty else None
    orgs_without_entries_count = (
        total_orgs_in_system - orgs_with_entries_count
        if total_orgs_in_system is not None
        else None
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Gesamtzahl Einträge", f"{total_entries:,}")
    with col2:
        st.metric("Einträge mit Organisationszuordnung", f"{entries_with_org:,}")
    with col3:
        st.metric("Organisationen mit Einträgen", f"{orgs_with_entries_count:,}")
    with col4:
        st.metric(
            "Organisationen ohne Einträge",
            f"{orgs_without_entries_count:,}" if orgs_without_entries_count else "–",
            help=f"Von insgesamt {total_orgs_in_system:,} registrierten Organisationen."
            if total_orgs_in_system
            else None
        )

    st.markdown("---")

    # -------------------------------------------------------
    # 1️⃣ Mehrfachauswahl
    # -------------------------------------------------------
    organisationen = sorted(df["Organisation"].dropna().unique())
    ausgewaehlte_orgs = st.multiselect(
        "🔍 Wähle eine oder mehrere Mitgliedsorganisationen:",
        organisationen,
        default=None,
        placeholder="Organisation(en) suchen oder eingeben …",
        help="Du kannst hier mehrere Organisationen gleichzeitig auswählen."
    )

    if not ausgewaehlte_orgs:
        st.info("Bitte wähle mindestens eine Mitgliedsorganisation aus, um die Auswertung zu starten.")
        return

    df_org = df[df["Organisation"].isin(ausgewaehlte_orgs)]

    # -------------------------------------------------------
    # 2️⃣ Gesamtanzahl der Angebote
    # -------------------------------------------------------
    st.subheader("🏙️ Übersicht")
    st.metric("Gesamtzahl der Angebote (Berlin)", f"{len(df_org):,}")

    # -------------------------------------------------------
    # 3️⃣ Verteilung nach Bezirken
    # -------------------------------------------------------
    if "Bezirk" in df_org.columns and df_org["Bezirk"].notna().any():
        bezirk_counts = df_org["Bezirk"].value_counts().reset_index()
        bezirk_counts.columns = ["Bezirk", "Anzahl"]

        fig_bzr = px.bar(
            bezirk_counts,
            x="Anzahl",
            y="Bezirk",
            orientation="h",
            text="Anzahl",
            color="Bezirk",
            color_discrete_sequence=["#0063A6"],
            title="Verteilung der Angebote nach Bezirken"
        )
        fig_bzr.update_traces(textposition="outside")
        fig_bzr.update_layout(showlegend=False, height=500)
        st.plotly_chart(fig_bzr, use_container_width=True)
    else:
        st.warning("Keine Bezirksinformationen verfügbar.")

    # -------------------------------------------------------
    # 4️⃣ Themenbereiche nach räumlicher Ebene (mit Übersetzung + Sozialräume)
    # -------------------------------------------------------
    st.markdown("---")
    st.subheader("🗂️ Themenbereiche nach räumlicher Ebene")

    # Themenübersetzung aus anderem Modul (falls dort definiert)
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

    # 🔹 Mögliche Raumebenen im Datensatz erkennen
    sozialraum_keys = [
        "planungsraum", "bezirksregion", "prognoseraum"
    ]

    # Spalten prüfen, die eine dieser Bezeichnungen enthalten
    sozialraum_spalten = [
        col for col in df_org.columns
        if any(key in col.lower() for key in sozialraum_keys)
    ]

    # Alle relevanten Ebenen zusammenführen (mit Bezirk + Stadtteil)
    potenzielle_spalten = ["Bezirk", "Stadtteil"] + sozialraum_spalten
    vorhandene_spalten = [c for c in potenzielle_spalten if c in df_org.columns]

    if not vorhandene_spalten:
        st.warning("Keine räumlichen Ebenen im Datensatz gefunden.")
    else:
        ausgewaehlte_ebene = st.selectbox(
            "📊 Ebene auswählen:",
            vorhandene_spalten,
            index=vorhandene_spalten.index("Bezirk") if "Bezirk" in vorhandene_spalten else 0,
            help="Wähle die Raumebene, auf der du die Themenverteilung sehen möchtest."
        )

        # Gruppierung nach gewählter Ebene
        grouped = (
            df_org.groupby([ausgewaehlte_ebene, "primaryTopic"])
            .size()
            .reset_index(name="Anzahl")
        )

        # Übersetzte Themenbezeichnung hinzufügen
        grouped["Thema (DE)"] = grouped["primaryTopic"].map(topic_translation).fillna(grouped["primaryTopic"])

        # Sortierung für saubere Anzeige
        grouped = grouped.sort_values(by=["Anzahl"], ascending=False)

        if not grouped.empty:
            fig_topics = px.bar(
                grouped,
                x="Anzahl",
                y=ausgewaehlte_ebene,
                color="Thema (DE)",
                orientation="h",
                title=f"Themenbereiche nach {ausgewaehlte_ebene}",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_topics.update_layout(
                barmode="stack",
                height=700,
                xaxis_title="Anzahl Angebote",
                yaxis_title=ausgewaehlte_ebene
            )
            st.plotly_chart(fig_topics, use_container_width=True)
        else:
            st.info("Keine Daten für die aktuelle Ebene gefunden.")
