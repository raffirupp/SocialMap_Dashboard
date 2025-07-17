# 📊 SocialMap Berlin Dashboard

Ein interaktives **Streamlit-Dashboard** zur Visualisierung der sozialen Angebote in Berlin – basierend auf der **offiziellen Social Map API**. Die Anwendung ermöglicht explorative Analysen nach Themen, Zeiträumen, Bezirken und mehr.

👉 **Live-Demo:**
[https://socialmapdashboard.streamlit.app/](https://socialmapdashboard.streamlit.app/)
*(Hinweis: Die Live-Version lädt die aktuellen Daten direkt aus der API.)*

---

## 🚀 Kurzanleitung

### 1️⃣ Repository klonen

```bash
git clone https://github.com/raffirupp/SocialMap_Dashboard.git
cd SocialMap_Dashboard
```

### 2️⃣ Lokale Installation

Python-Umgebung aktivieren (z. B. mit `venv` oder `conda`), dann:

```bash
pip install -r requirements.txt
```

### 3️⃣ Streamlit-App lokal starten

```bash
streamlit run Pari_Dashboard.py
```

---

## 🌐 Deployment auf Streamlit Cloud

1. **GitHub-Repository öffentlich stellen** oder der Streamlit Cloud Zugriff gewähren.
2. Auf [https://streamlit.io/cloud](https://streamlit.io/cloud) einloggen.
3. Über „New App“ das GitHub-Repo auswählen.
4. Als Hauptdatei `Pari_Dashboard.py` angeben.
5. Deployment starten und den Link teilen! 🎉

---

## 🗂️ Projektstruktur

```
SocialMap_Dashboard/
├── Pari_Dashboard.py                # Haupt-Streamlit-App
├── requirements.txt                 # Python-Abhängigkeiten
├── .streamlit/
│   └── config.toml                  # Optionale Streamlit-Konfiguration
├── modules/
│   ├── fetch_data.py                # Lädt Daten aus API oder Fallback-Datei
│   ├── plz_mapping.py               # Mapping: PLZ zu Bezirken & Stadtteilen
│   ├── einleitung.py                # Einführungsbereich & Gesamtübersicht
│   ├── zeitliche_analyse.py         # Analyse nach Änderungsdatum
│   ├── kategorien.py                # Thematische Kategorisierung
│   └── email_domains.py             # Analyse von E-Mail-Domains
├── data/
│   ├── api_snapshot.csv             # Optionaler Fallback-Datensatz
│   ├── PLZ_Matching.xlsx            # Mapping-Datei für PLZ & Bezirke
│   └── berlin_plz.geojson           # Optional: Geo-Daten für Karten
├── assets/
│   └── styles.css                   # Optional: individuelle CSS-Styles
└── README.md                        # Diese Datei
```

---

## 🛋️ Abhängigkeiten

Die notwendigen Pakete sind in `requirements.txt` definiert, z. B.:

* `streamlit` – App-Framework
* `pandas` – Datenanalyse
* `requests` – API-Anbindung
* `plotly` – interaktive Visualisierungen
* `openpyxl` – Excel-Unterstützung

---

## 🔎 Datengrundlage

Die Daten stammen von der öffentlichen API der **Social Map Berlin**:

> [https://public.socialmap-berlin.de/items](https://public.socialmap-berlin.de/items)

Die API liefert:

* Angebote sozialer Träger & Initiativen in Berlin
* Informationen wie Name, Adresse, Thema (`primaryTopic`), Bezirk, letzter Bearbeitungsstand (`lastEditDate`) und mehr.

Wenn die API nicht erreichbar ist, wird automatisch der **Fallback-Datensatz (`data/api_snapshot.csv`)** verwendet.

Die Zuordnung von Postleitzahlen zu Bezirken/Stadtteilen basiert auf der Datei:

> `data/PLZ_Matching.xlsx`

---

## 📝 Hinweise zur Nutzung

* Die App lädt und analysiert stets die **aktuellsten API-Daten**.
* Bei Bedarf kann das Projekt auch einfach um weitere Analysen oder Visualisierungen erweitert werden.
* Die **PNG-Exportfunktion** wurde entfernt, um die Kompatibilität mit der **Streamlit Cloud** sicherzustellen.
* Die Visualisierungen sind interaktiv und können direkt in der App exploriert werden.

---

## 🌐 Live-Demo

👉 [Hier klicken, um das Dashboard live zu testen](https://socialmapdashboard.streamlit.app/)

---
