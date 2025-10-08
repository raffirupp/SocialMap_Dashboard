# modules/plz_mapping.py

import pandas as pd

def load_mapping(path: str = 'data/berlin_plz_to_sozialraum.xlsx') -> pd.DataFrame:
    """
    Liest die Excel-Tabelle mit dem Berliner PLZ-zu-Sozialraum-Mapping ein
    (z. B. 'berlin_plz_to_sozialraum.xlsx') und gibt ein DataFrame zurück.

    Erwartete Spalten:
    ['PLZ', 'Bezirk', 'Stadtteil', 'PLR_ID', 'Planungsraum_Name',
     'BZR_ID', 'Bezirksregion_Name', 'PGR_ID', 'Prognoseraum_Name', 'Bezirk_Name']

    Rückgabe: DataFrame mit allen gefundenen Spalten.
    """
    try:
        # Lies explizit das Sheet "Sheet1" (aktueller Stand deiner Datei)
        df_map = pd.read_excel(path, sheet_name="Sheet1", dtype=str)
        df_map.columns = df_map.columns.str.strip()
        #print(f"✅ Mapping-Datei geladen: {len(df_map)} Zeilen (Sheet: Sheet1)")

        # Sicherstellen, dass PLZ als String vorliegt
        if 'PLZ' in df_map.columns:
            df_map['PLZ'] = df_map['PLZ'].astype(str).str.strip()
            df_map = df_map[df_map['PLZ'].str.match(r'^\d{5}$', na=False)]
        else:
            raise ValueError("Spalte 'PLZ' nicht gefunden.")

        # Optional: nur relevante Spalten behalten, falls einige fehlen
        expected_cols = [
            'PLZ', 'Bezirk', 'Stadtteil',
            'PLR_ID', 'Planungsraum_Name',
            'BZR_ID', 'Bezirksregion_Name',
            'PGR_ID', 'Prognoseraum_Name', 'Bezirk_Name'
        ]
        available_cols = [c for c in expected_cols if c in df_map.columns]
        df_map = df_map[available_cols]

        #print(f"📋 Verfügbare Spalten im Mapping: {', '.join(available_cols)}")

        return df_map

    except Exception as e:
        print(f"⚠️ Fehler beim Laden des Mappings: {e}")
        return pd.DataFrame(columns=['PLZ', 'Bezirk', 'Stadtteil'])


if __name__ == "__main__":
    # Schnelltest
    mapping = load_mapping('data/berlin_plz_to_sozialraum.xlsx')
    print(mapping.head())  # prüfen, dass PLZ, Bezirk etc. vorhanden sind
