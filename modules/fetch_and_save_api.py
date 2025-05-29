import requests
import pandas as pd

# API-URL
url = "https://public.socialmap-berlin.de/items"

try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()

    # Die API liefert offenbar in 'items' die eigentlichen Daten
    items = data.get("items", [])
    if not items:
        print("⚠️ Achtung: Es wurden keine Items in der API gefunden!")
    else:
        # In DataFrame umwandeln und als CSV speichern
        df = pd.json_normalize(items)
        df.to_csv("data/api_snapshot.csv", index=False)
        print(f"✅ API-Daten erfolgreich als 'data/api_snapshot.csv' gespeichert. Anzahl: {len(df)}")

except Exception as e:
    print(f"❌ Fehler beim Abrufen der API: {e}")
