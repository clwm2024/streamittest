import os
from dotenv import load_dotenv

# .env-Datei laden
load_dotenv('settings.env')

# API-Key aus der Umgebungsvariablen abrufen
api_key = os.getenv('OPENAI_API_KEY')

print(f"Dein API-Key ist: {api_key}")
