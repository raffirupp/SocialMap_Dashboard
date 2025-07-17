# Streamlit App zur Analyse von Socialmap-Daten mit PLZ-Overlay

import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
from urllib.parse import urlencode
import json

st.set_page_config(page_title="Socialmap Dashboard Berlin", layout="wide")
st.title("📍 Socialmap Dashboard Berlin")

# --- Datenquellen laden ---

@st.cache_data
def load_berlin_plz():
    base_url = "https://fbinter.stadt-berlin.de/fb/wfs/data/senstadt/s_plz"
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "TYPENAMES": "s_plz",
        "outputFormat": "application/json"
    }
    url = base_url + "?" + urlencode(params)
    return gpd.read_file(url)

@st.cache_data
def load_socialmap_json():
    with open("/Users/raffaelruppert/Desktop/Datenanalyse/Social MAP/items.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    if isinstance(data, dict):
        data = data.get("data", [])
    return pd.DataFrame(data)

# --- Daten laden ---
plz_gdf = load_berlin_plz()
df = load_socialmap_json()

if df.empty:
    st.warning("Keine Daten geladen. Bitte Datei überprüfen.")
    st.stop()

# --- Daten vorbereiten ---

# Zeitspalten umwandeln (sicherer)
if 'creationDate' in df.columns:
    df['creationDate'] = pd.to_numeric(df['creationDate'], errors='coerce')
    df = df[df['creationDate'] < 1e13]
    df['creationDate'] = pd.to_datetime(df['creationDate'], unit='ms')

if 'lastEditDate' in df.columns:
    df['lastEditDate'] = pd.to_numeric(df['lastEditDate'], errors='coerce')
    df = df[df['lastEditDate'] < 1e13]
    df['lastEditDate'] = pd.to_datetime(df['lastEditDate'], unit='ms')

# E-Mail-Domains extrahieren
if 'email' in df.columns:
    df['email'] = df['email'].astype(str)
    df['domain'] = df['email'].str.extract(r'@(.+)$')

# --- Visualisierung: Zeitverlauf ---
st.subheader("📅 Verteilung der Erstellungsdaten")
fig = px.histogram(df, x='creationDate', nbins=50, title="Verteilung der Erstellungszeitpunkte")
st.plotly_chart(fig, use_container_width=True)

# --- Visualisierung: State & Primary Topic ---
st.subheader("🏷️ Häufigkeiten von 'state' und 'primaryTopic'")
col1, col2 = st.columns(2)

if 'state' in df.columns:
    with col1:
        state_counts = df['state'].value_counts().reset_index()
        state_counts.columns = ['state', 'count']
        fig_state = px.bar(state_counts, x='state', y='count',
                           labels={'state': 'State', 'count': 'Anzahl'},
                           title="Verteilung der 'state'-Werte")
        st.plotly_chart(fig_state, use_container_width=True)

if 'primaryTopic' in df.columns:
    with col2:
        topic_counts = df['primaryTopic'].value_counts().reset_index()
        topic_counts.columns = ['primaryTopic', 'count']
        fig_topic = px.bar(topic_counts, x='primaryTopic', y='count',
                           labels={'primaryTopic': 'Topic', 'count': 'Anzahl'},
                           title="Verteilung der 'primaryTopic'-Werte")
        st.plotly_chart(fig_topic, use_container_width=True)

# --- Visualisierung: Top Domains ---
if 'domain' in df.columns:
    st.subheader("✉️ Top 10 E-Mail-Domains")
    top10_domains = df['domain'].value_counts().head(10).reset_index()
    top10_domains.columns = ['domain', 'count']
    fig_domains = px.bar(top10_domains, x='domain', y='count', labels={'domain': 'Domain', 'count': 'Anzahl'},
                         title="Top 10 Domains")
    st.plotly_chart(fig_domains, use_container_width=True)

# --- GeoMap Placeholder ---
st.subheader("🌍 Geodaten (PLZ-Gebiete in Berlin)")
with st.expander("PLZ-Gebiete anzeigen"):
    st.write(plz_gdf.head())
    st.map(plz_gdf.to_crs(epsg=4326).set_geometry('geometry'))
