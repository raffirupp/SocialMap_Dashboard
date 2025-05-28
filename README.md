🚀 Kurzanleitung
1️⃣ Repository klonen
bash
Code kopieren
git clone https://github.com/raffirupp/SocialMap_Dashboard.git
cd SocialMap_Dashboard
2️⃣ Lokale Installation
Aktiviere deine Python-Umgebung (z. B. conda oder venv).

Installiere die Abhängigkeiten:

bash
Code kopieren
pip install -r requirements.txt
3️⃣ Streamlit-App starten
bash
Code kopieren
streamlit run Pari_Dashboard.py
🌐 Streamlit Cloud Deployment
Stelle sicher, dass dein GitHub-Repo öffentlich ist oder Streamlit Cloud Zugriff darauf hat.

Logge dich bei Streamlit Cloud ein.

Klicke auf "New App", wähle dein Repo und die Datei Pari_Dashboard.py als Haupt-Datei.

Starte das Deployment und teile den Link zur App! 🎉

🗂️ Ordnerstruktur
plaintext
Code kopieren
SocialMap_Dashboard/
├── Pari_Dashboard.py                # Haupt-Streamlit-App
├── requirements.txt                 # Python-Abhängigkeiten
├── .streamlit/
│   └── config.toml                  # Streamlit-Konfiguration
├── modules/
│   ├── __init__.py
│   ├── fetch_data.py                # Daten-Import aus Social Map API
│   ├── plz_mapping.py               # PLZ-Mapping für Bezirke/Stadtteile
│   ├── einleitung.py                # Einführung und Charts
│   ├── zeitliche_analyse.py         # Zeitliche Analysen
│   ├── kategorien.py                # Thematische Auswertungen
│   └── email_domains.py             # E-Mail-Domain-Auswertungen
├── data/
│   ├── PLZ_Matching.xlsx            # Mapping-Datei für PLZ/Bezirke/Stadtteile
│   └── berlin_plz.geojson           # Optional: Geo-Daten
├── assets/
│   └── styles.css                   # Optional: eigene Styles
└── README.md                        # Diese Datei
📦 Abhängigkeiten
Alle notwendigen Python-Pakete sind in der Datei requirements.txt definiert.
Beispiele:

streamlit

pandas

requests

plotly

openpyxl

📝 Hinweise
Das Dashboard lädt die Daten live aus der API: https://public.socialmap-berlin.de/items

Bei instabiler Internetverbindung oder Timeouts kann ein Fallback aktiviert sein.

Die Datei PLZ_Matching.xlsx ist essenziell für die Zuordnung von Postleitzahlen zu Berliner Bezirken und Stadtteilen.

🌐 Live-Demo
(Link ausstehend)
Hier klicken, um das Dashboard live zu testen!