# modules/fetch_data.py
import pandas as pd
import requests
import streamlit as st

ITEMS_URL = "https://public.socialmap-berlin.de/items"
OPTIONS_URL = "https://api.socialmap-berlin.de/options"
FALLBACK_PATH = "data/api_snapshot.csv"


# ---------------------------
# Hilfsfunktionen
# ---------------------------

def extract_org_tag(tags):
    """Extrahiert den Organisationstag (z. B. o_ri_freiraum) aus der Tagliste."""
    if isinstance(tags, list):
        for tag in tags:
            if isinstance(tag, str) and tag.startswith("o_ri_"):
                return tag
    return None


@st.cache_data(ttl=86400)  # 24 Stunden Cache
def load_options():
    """Lädt Organisationsinformationen (o_ri_*) aus der Options-API."""
    try:
        r = requests.get(OPTIONS_URL, timeout=30)
        r.raise_for_status()
        data = r.json()
        df_opts = pd.DataFrame(data)

        # Nur Organisationen (key == 'ri')
        df_opts = df_opts[df_opts["key"] == "ri"]

        # Relevante Spalten vereinheitlichen
        df_opts = df_opts[["tag", "label"]].rename(columns={"tag": "id", "label": "title"})

        print(f"✅ Options geladen: {len(df_opts)} Organisationen")
        return df_opts

    except Exception as e:
        print(f"⚠️ Fehler beim Laden der Options-API: {e}")
        return pd.DataFrame(columns=["id", "title"])


# ---------------------------
# Hauptfunktion: Items + Merge mit Organisationen
# ---------------------------

@st.cache_data(ttl=3600)  # 1 Stunde Cache
def load_items():
    """Lädt Items aus der Socialmap-API, reichert sie mit Organisationsnamen an
    und nutzt lokale Fallback-Datei bei Fehlern.
    """
    data_source = "API"

    try:
        response = requests.get(ITEMS_URL, timeout=30)
        response.raise_for_status()
        data = response.json()

        print(f"✅ API-Antwortgröße: {len(response.content)/1024:.2f} KB")
        print(f"🔢 Anzahl Items (roh): {len(data)}")

        # Falls API verschachtelt ist (z. B. {"items": [...]})
        if isinstance(data, dict) and "items" in data:
            data = data["items"]
            print(f"📥 Anzahl Items extrahiert: {len(data)}")

        if not data:
            raise ValueError("⚠️ API-Daten sind leer.")

        df = pd.json_normalize(data)
        print(f"✅ Daten erfolgreich aus der API geladen. Anzahl Zeilen: {len(df)}")

    except Exception as e:
        print(f"⚠️ Fehler beim Laden der API: {e}")
        print(f"📂 Versuche stattdessen Daten aus {FALLBACK_PATH} zu laden...")
        data_source = "Fallback"

        try:
            df = pd.read_csv(FALLBACK_PATH)
            print(f"✅ Fallback-Daten erfolgreich geladen. Anzahl Zeilen: {len(df)}")
        except Exception as fallback_e:
            print(f"❌ Fehler beim Laden des Fallbacks: {fallback_e}")
            df = pd.DataFrame()  # Leerer DataFrame als Notlösung

    # Datumsspalten konvertieren
    for col in ["lastEditDate", "projectStartDate"]:
        if col in df.columns:
            try:
                df[col] = pd.to_datetime(pd.to_numeric(df[col], errors="coerce"), unit="ms", errors="coerce")
            except Exception as e:
                print(f"⚠️ Fehler beim Konvertieren von {col}: {e}")
                df[col] = pd.NaT
        else:
            print(f"ℹ️ Spalte {col} nicht vorhanden.")

    # Domain aus Email extrahieren
    if "email" in df.columns:
        df["domain"] = df["email"].str.extract(r"@([\w\.-]+)").fillna("")

    # Organisationstag aus Tags extrahieren
    if "tags" in df.columns:
        df["org_tag"] = df["tags"].apply(extract_org_tag)
    else:
        df["org_tag"] = None

    # Options laden und joinen
    df_opts = load_options()
    if not df_opts.empty:
        df = df.merge(df_opts, how="left", left_on="org_tag", right_on="id", suffixes=("", "_org"))
        df.rename(columns={"title_org": "Organisation"}, inplace=True)
        print(f"✅ Organisationen zugeordnet: {df['Organisation'].notna().sum()} / {len(df)} Items")
    else:
        df["Organisation"] = None
        print("⚠️ Keine Organisationsdaten verfügbar – Zuordnung übersprungen.")

    return df, data_source
