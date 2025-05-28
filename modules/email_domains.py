import streamlit as st
import plotly.express as px
import pandas as pd
from io import BytesIO

def show_email_domains(df):
    st.header("✉️ E-Mail-Domains: Auswertung")

    # Nur gültige Mails mit Domain extrahieren
    df_valid = df[df['email'].notna() & df['email'].str.contains("@")].copy()
    df_valid["domain"] = df_valid["email"].str.extract(r"@([\w\.-]+)").fillna("")

    # 🔹 1. Berlinweite Verteilung (Top 10 Domains)
    st.subheader("🌐 Top 10 Domains Berlin-weit")

    top_domains = df_valid["domain"].value_counts().nlargest(10).reset_index()
    top_domains.columns = ["Domain", "Anzahl"]

    fig = px.bar(
        top_domains,
        x="Domain",
        y="Anzahl",
        text="Anzahl",
        title="Häufigste E-Mail-Domains (gesamt)"
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    # 🔹 2. Domain-Verteilung im Bezirk (ohne Stadtteile)
    st.markdown("---")
    st.subheader("🏘️ Domain-Verteilung im ausgewählten Bezirk")

    bezirke = sorted(df_valid['Bezirk'].dropna().unique())
    selected_bezirk = st.selectbox("Bezirk auswählen:", bezirke)

    df_bzr = df_valid[df_valid['Bezirk'] == selected_bezirk]

    if df_bzr.empty:
        st.info("Keine gültigen E-Mails für diesen Bezirk.")
        return

    domain_counts = df_bzr["domain"].value_counts().nlargest(10).reset_index()
    domain_counts.columns = ["Domain", "Anzahl"]

    fig2 = px.bar(
        domain_counts,
        x="Domain",
        y="Anzahl",
        text="Anzahl",
        title=f"Top 10 E-Mail-Domains in {selected_bezirk}"
    )
    fig2.update_traces(textposition="outside")
    fig2.update_layout(
        xaxis_title="Domain",
        yaxis_title="Anzahl",
        xaxis_tickangle=-45,
        showlegend=False
    )

    st.plotly_chart(fig2, use_container_width=True)
    # 🔹 3. Datenexport (Excel)
    st.markdown("---")
    st.subheader("📥 E-Mail-Adressen herunterladen")

    export_option = st.radio(
        "Welche Daten möchtest du herunterladen?",
        [
            "Gesamtliste (alle Mail-Adressen mit Zuordnung zu Bezirk und Stadtteil)",
            f"Gefiltert nach Bezirk: {selected_bezirk}"
        ]
    )

    if export_option.startswith("Gesamtliste"):
        export_df = df_valid[["Bezirk", "Stadtteil", "email"]].dropna()
    else:
        export_df = df_bzr[["Stadtteil", "email"]].dropna()

    # Als Excel speichern
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        export_df.to_excel(writer, index=False)
    output.seek(0)

    st.download_button(
        label="📁 Download als Excel",
        data=output,
        file_name="email_adressen.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
