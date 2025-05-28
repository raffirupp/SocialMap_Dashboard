import pandas as pd
import requests

def load_items():
    url = "https://public.socialmap-berlin.de/items"
    response = requests.get(url)
    data = response.json()

    df = pd.json_normalize(data)

    for col in ["lastEditDate", "projectStartDate"]:
        if col in df.columns:
            # Prüfen, ob überhaupt Werte da sind
            if df[col].notna().sum() > 0:
                try:
                    # Nur die Zeilen, die numerisch sind (oder wo es Sinn macht)
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                    # NaN (nicht umwandelbar) bleibt NaT
                    df[col] = pd.to_datetime(df[col], unit="ms", errors="coerce")
                except Exception as e:
                    print(f"Fehler bei Spalte {col}: {e}")
                    df[col] = pd.NaT  # Setze alles auf NaT bei Fehler
            else:
                print(f"Spalte {col} ist leer oder hat keine gültigen Werte.")
                df[col] = pd.NaT
        else:
            print(f"Spalte {col} ist nicht vorhanden.")
            df[col] = pd.NaT

    # Domain extrahieren
    if "email" in df.columns:
        df["domain"] = df["email"].str.extract(r"@([\w\.-]+)").fillna("")

    return df
