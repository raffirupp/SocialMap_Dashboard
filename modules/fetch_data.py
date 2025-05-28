import pandas as pd
import requests

def load_items():
    url = "https://public.socialmap-berlin.de/items"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"✅ API-Antwortgröße: {len(response.content)/1024:.2f} KB")
        print(f"🔢 Anzahl Items: {len(data)}")
        
        # Wenn API 'items' enthält, extrahiere nur diese
        items = data.get('items', [])
        print(f"🔢 Anzahl Einträge: {len(items)}")

    except Exception as e:
        print(f"⚠️ Fehler beim Abrufen der API-Daten: {e}")
        items = []

    if not items:
        print("⚠️ Achtung: Keine Daten geladen. Das Dashboard zeigt keine Einträge.")
        return pd.DataFrame()

    # Daten normalisieren (verschachtelte JSON in flache Tabelle)
    df = pd.json_normalize(items)
    print(f"🔎 Spalten im DataFrame: {list(df.columns)}")
    print(f"🔢 Anzahl Zeilen: {len(df)}")

    # Datumsfelder umwandeln – robust und fehlervermeidend
    for col in ["lastEditDate", "projectStartDate"]:
        if col in df.columns:
            print(f"🔍 Spalte {col} gefunden. Konvertiere Werte.")
            # Sicherstellen, dass nur gültige Zahlen (z.B. Unix-Millisekunden) verarbeitet werden
            numeric_mask = pd.to_numeric(df[col], errors='coerce').notna()
            print(f"🔢 Gültige Werte für {col}: {numeric_mask.sum()} von {len(df)}")
            if numeric_mask.any():
                df.loc[numeric_mask, col] = pd.to_datetime(df.loc[numeric_mask, col], unit='ms', errors='coerce')
                df.loc[~numeric_mask, col] = pd.NaT
            else:
                print(f"⚠️ Spalte {col} enthält keine gültigen numerischen Werte. Setze alle auf NaT.")
                df[col] = pd.NaT
        else:
            print(f"⚠️ Spalte {col} nicht vorhanden. Setze alle Werte auf NaT.")
            df[col] = pd.NaT

    # E-Mail-Domains extrahieren, falls Spalte vorhanden
    if "email" in df.columns:
        df["domain"] = df["email"].str.extract(r"@([\w\.-]+)").fillna("")
    else:
        print("⚠️ Spalte 'email' fehlt – keine Domains extrahiert.")

    return df
