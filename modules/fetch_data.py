import pandas as pd
import requests

def load_items():
    url = "https://public.socialmap-berlin.de/items"
    fallback_path = "data/api_snapshot.csv"
    data_source = "API"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        print(f"✅ API-Antwortgröße: {len(response.content)/1024:.2f} KB")
        print(f"🔢 Anzahl Items (roh): {len(data)}")

        # Extrahiere die tatsächlichen Items aus dem JSON
        if isinstance(data, dict) and "items" in data:
            data = data["items"]
            print(f"📥 Anzahl Items extrahiert: {len(data)}")

        if not data:
            raise ValueError("⚠️ API-Daten sind leer.")

        df = pd.json_normalize(data)
        print(f"✅ Daten erfolgreich aus der API geladen. Anzahl Zeilen: {len(df)}")

    except Exception as e:
        print(f"⚠️ Fehler beim Laden der API: {e}")
        print(f"📂 Versuche stattdessen Daten aus {fallback_path} zu laden...")
        data_source = "Fallback"

        try:
            df = pd.read_csv(fallback_path)
            print(f"✅ Fallback-Daten erfolgreich geladen. Anzahl Zeilen: {len(df)}")
        except Exception as fallback_e:
            print(f"❌ Fehler beim Laden des Fallbacks: {fallback_e}")
            df = pd.DataFrame()  # Leerer DataFrame als Notlösung

    # Datumsspalten verarbeiten
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

    return df, data_source  # Rückgabe von DataFrame und Datenquelle
