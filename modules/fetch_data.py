import pandas as pd
import requests

def load_items():
    url = "https://public.socialmap-berlin.de/items"
    try:
        response = requests.get(url, timeout=30)  # Timeout verlängert
        response.raise_for_status()
        data = response.json()

        print(f"✅ API-Antwortgröße: {len(response.content) / 1024:.2f} KB")
        print(f"🔢 Anzahl Items: {len(data)}")
        
        # Analysiere die Struktur der API
        print(f"🔍 API-Daten: {data.keys()}")
        items = data.get("items", [])
        print(f"🔢 Anzahl items: {len(items)}")

    except Exception as e:
        print(f"⚠️ Fehler beim Laden der API: {e}")
        items = [
            {"title": "Test-Eintrag", "zip": "10115", "lastEditDate": 1622547800000}
        ]

    if not items:
        print("⚠️ Achtung: Keine Items aus API geladen. Leere DataFrame wird zurückgegeben.")
        return pd.DataFrame()

    df = pd.json_normalize(items)
    print(f"🔎 Spalten im DataFrame: {list(df.columns)}")
    print(f"🔢 Anzahl Zeilen: {len(df)}")

    # Datumsspalten umwandeln, robust gegen fehlerhafte Werte
    for col in ["lastEditDate", "projectStartDate"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            valid_values = df[col].dropna()
            if not valid_values.empty:
                print(f"🔍 Spalte {col}: Max: {valid_values.max()}, Min: {valid_values.min()}")
                df[col] = pd.to_datetime(df[col], unit='ms', errors='coerce')
            else:
                print(f"⚠️ Spalte {col} enthält keine gültigen numerischen Werte.")
                df[col] = pd.NaT
        else:
            print(f"⚠️ Spalte {col} fehlt in den Daten. Spalte wird mit NaT gefüllt.")
            df[col] = pd.NaT

    # Domain extrahieren
    if "email" in df.columns:
        df["domain"] = df["email"].str.extract(r"@([\w\.-]+)").fillna("")
    else:
        print("⚠️ Spalte 'email' fehlt – keine Domains extrahiert.")

    return df
