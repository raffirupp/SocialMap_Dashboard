import pandas as pd
import requests

def load_items():
    """
    Holt die Daten von der Social Map API und wandelt sie in ein DataFrame um.
    """
    url = "https://public.socialmap-berlin.de/items"
    response = requests.get(url)
    data = response.json()

    # JSON in DataFrame umwandeln
    df = pd.json_normalize(data)

    # Optional: Zeige die Spalten
    # print("Spalten:", df.columns.tolist())

    # Zeitspalten umwandeln
    for col in ["lastEditDate", "projectStartDate"]:
        if col in df.columns:
            # Prüfen, ob es überhaupt gültige Werte gibt
            if df[col].notna().sum() > 0:
                try:
                    # Sicherstellen, dass die Werte numerisch sind
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                    # Dann zu datetime konvertieren
                    df[col] = pd.to_datetime(df[col], unit="ms", errors="coerce")
                except Exception as e:
                    print(f"Fehler bei Spalte {col}: {e}")
            else:
                print(f"Spalte {col} ist leer oder hat keine gültigen Werte.")
        else:
            print(f"Spalte {col} ist nicht im DataFrame enthalten.")

    # E-Mail-Domain extrahieren (optional)
    if "email" in df.columns:
        df["domain"] = df["email"].str.extract(r"@([\w\.-]+)").fillna("")

    return df
