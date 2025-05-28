import pandas as pd


def load_mapping(path: str) -> pd.DataFrame:
    """
    Liest die Excel-Tabelle PLZ_Matching.xlsx (Sheet 'PLZ_Matching') ein,
    splittet die PLZ-Listen und entfernt Leerzeichen, 
    gibt ein DataFrame mit den Spalten ['PLZ', 'Bezirk', 'Stadtteil'] zurück.
    """
    # Excel einlesen
    df_map = pd.read_excel(path, sheet_name='PLZ_Matching', dtype=str)
    # PLZ-Feld: Punkte zu Kommas ersetzen, dann splitten
    df_map['PLZ'] = (
        df_map['PLZ']
        .str.replace('.', ',', regex=False)
        .str.split(r"\s*,\s*")
    )
    # Explodiere in einzelne Zeilen
    df_map = df_map.explode('PLZ').reset_index(drop=True)
    # Leerzeichen entfernen
    df_map['PLZ'] = df_map['PLZ'].str.strip()
    # Nur 5-stellige numerische PLZ behalten
    df_map = df_map[df_map['PLZ'].str.match(r'^\d{5}$')]
    return df_map


if __name__ == "__main__":
    # Schnelltest
    mapping = load_mapping('data/PLZ_Matching.xlsx')
    print(mapping.head())  # prüfen, dass PLZ, Bezirk und Stadtteil existieren
