import requests
import pandas as pd

def load_items() -> pd.DataFrame:
    """Lädt das JSON von public.socialmap-berlin.de/items und gibt es als DataFrame zurück."""
    url = "https://public.socialmap-berlin.de/items"
    resp = requests.get(url)
    resp.raise_for_status()
    payload = resp.json()

    # Extrahiere Liste
    if isinstance(payload, dict):
        items = payload.get("items") or payload.get("data")
        if items is None:
            for v in payload.values():
                if isinstance(v, list):
                    items = v
                    break
        if items is None:
            raise ValueError("Keine Liste von Einträgen gefunden.")
    else:
        items = payload

    # Flachmachen
    df = pd.json_normalize(items)

    # Datumsspalten nur dann konvertieren, wenn vorhanden
    date_cols = ["lastEditDate", "projectStartDate", "projectEndDate", "resubmissionDate"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], unit="ms", errors="coerce")

    # Email-Domain
    if "email" in df.columns:
        df["email"] = df["email"].astype(str)
        df["domain"] = df["email"].str.split("@").str[1].fillna("")

    return df
