from modules.fetch_data import load_items

if __name__ == "__main__":
    df = load_items()
    print(f"📊 Geladene Zeilen: {len(df)}")
    print("🔎 Spalten:", list(df.columns))
    print(df.head())
