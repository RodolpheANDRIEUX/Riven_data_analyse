import sqlite3

# Connexion à la base de données (créée si elle n'existe pas)
conn = sqlite3.connect("riven_stats.db")
cursor = conn.cursor()

# Création de la table des matchs
cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    server TEXT,
    player_name TEXT,
    tag TEXT,
    puuid TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
player INTEGER REFERENCES players(id),
match_id TEXT
)
""")

# Sauvegarde et fermeture de la connexion
conn.commit()
conn.close()

print("✅ Base de données et table créées avec succès !")
