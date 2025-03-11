import sqlite3

import requests
import time
import json

# Configuration API Riot
RIOT_API_KEY = "RGAPI-4a05d71e-00d6-4efd-b40b-d50c9740564c"
RIOT_API_URL = "https://europe.api.riotgames.com"

with open("riven_players_euw.txt", "r", encoding="utf-8") as f:
    players = [line.strip() for line in f.readlines()]

# Headers pour API Riot
HEADERS = {"X-Riot-Token": RIOT_API_KEY}
conn = sqlite3.connect("riven_stats.db")
cursor = conn.cursor()

# vider la table players et matches
cursor.execute("""
DELETE FROM players
""")
cursor.execute(""" 
DELETE FROM matches
""")
conn.commit()


def request_riot_api(url):
    while True:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 429:  # Trop de requêtes
            retry_after = int(response.headers.get("Retry-After", 2))
            print(f"Rate limit atteint, pause de {retry_after} secondes...")
            time.sleep(retry_after)
        elif response.status_code != 200:
            print(f"Erreur {response.status_code}: {response.text}")
            return None
        else:
            return response.json()


# Stockage des données
all_data = []

for player_name in players:
    print(f"\n🔍 Traitement du joueur : {player_name}")

    # Séparer le nom du tag
    gameName, tagLine = player_name.split("#")

    # 1️⃣ Récupérer PUUID du joueur
    summoner_url = f"{RIOT_API_URL}/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
    summoner_data = request_riot_api(summoner_url)

    if not summoner_data:
        print(f"⚠️ Impossible de récupérer {player_name}, on passe au suivant.")
        continue

    puuid = summoner_data["puuid"]

    #inserer en db
    cursor.execute("INSERT INTO players (server, player_name, tag, puuid) VALUES (?, ?, ?, ?)",
                   ("euw", gameName, tagLine, puuid))
    conn.commit()

    # 2️⃣ Récupérer les derniers matchs
    matchlist_url = f"{RIOT_API_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids?count=100"
    match_ids = request_riot_api(matchlist_url)

    if not match_ids:
        print(f"⚠️ Aucun match trouvé pour {player_name}.")
        continue

    player_id = cursor.lastrowid

    for match_id in match_ids:
        cursor.execute("INSERT INTO matches (player, match_id) VALUES (?, ?)", (player_id, match_id))
        conn.commit()

print("\n✅ Données sauvegardées dans riven_stats.db !")
