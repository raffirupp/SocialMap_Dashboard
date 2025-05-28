import streamlit as st
import pandas as pd

def show_unmatched(df):
    st.header("🧩 Unzugeordnete Einträge")

    # Alle Einträge mit PLZ, aber ohne Bezirk
    mask = df['Postleitzahl'].notna() & df['Bezirk'].isna()
    missing_bzr = df[mask]

    st.markdown("### Einträge mit PLZ, aber ohne Bezirk")
    st.markdown(f"Anzahl: **{len(missing_bzr)}**")
    st.dataframe(
        missing_bzr[[
            'title',
            'Postleitzahl',
            'Stadtteil',
            'email',
            'website'
        ]].head(20)
    )

    # Unmatched mit Präfix 10–14
    prefixes = ['10', '11', '12', '13', '14']
    missing_pref = missing_bzr[missing_bzr['Postleitzahl'].str[:2].isin(prefixes)]

    st.markdown("### Unmatched-Einträge mit PLZ beginnend mit 10–14")
    st.markdown(f"Anzahl: **{len(missing_pref)}**")
    st.markdown("**Fehlende PLZ (unique):**")
    st.write(sorted(missing_pref['Postleitzahl'].unique().tolist()))
    st.dataframe(
        missing_pref[[
            'title',
            'Postleitzahl',
            'Stadtteil',
            'email',
            'website'
        ]].head(20)
    )
