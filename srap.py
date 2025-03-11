import requests
from bs4 import BeautifulSoup
import time
import random

# URL de base pour les pages de classement de Riven sur EUW
BASE_URL = "https://www.leagueofgraphs.com/fr/rankings/summoners/riven/euw/page-{}"

# Nombre total de pages à scraper
TOTAL_PAGES = 50

# Liste pour stocker les noms des joueurs
players = []

# User-Agent pour simuler un navigateur
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Scraping des pages
for page in range(1, TOTAL_PAGES + 1):
    url = BASE_URL.format(page)
    print(f"Scraping page {page}...")
    try:
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 403:
            print("⚠️ Accès refusé (403) - Essaye un VPN ou une IP différente")
            break
        elif response.status_code != 200:
            print(f"Erreur {response.status_code} sur la page {page}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraction des noms de joueurs depuis <span class="name">
        for player_tag in soup.select('td a div.txt span.name'):
            player_name = player_tag.text.strip()
            if player_name:
                players.append(player_name)

        # Pause aléatoire entre les requêtes pour éviter d'être détecté comme bot
        time.sleep(random.uniform(2, 5))

    except Exception as e:
        print(f"Erreur lors du scraping de la page {page}: {e}")
        continue

    print(f"\n{len(players)} joueurs récupérés !")


# Affichage du résultat
print(f"\n{len(players)} joueurs récupérés !")
print(players[:20])  # Afficher les 20 premiers joueurs

# Sauvegarde dans un fichier
with open("riven_players_euw.txt", "w", encoding="utf-8") as f:
    for player in players:
        f.write(player + "\n")

print("Liste enregistrée dans 'riven_players_euw.txt'.")
