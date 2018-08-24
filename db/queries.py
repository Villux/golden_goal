create_elo_table = '''CREATE TABLE elo_table
                    (id integer PRIMARY KEY AUTOINCREMENT,
                    date TIMESTAMP, team text, elo real,
                    match_id integer,
                    FOREIGN KEY(match_id) REFERENCES match_table(id));'''

drop_elo_table = "DROP TABLE IF EXISTS elo_table;"

create_odds_table = '''CREATE TABLE odds_table
                    (id integer PRIMARY KEY AUTOINCREMENT,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    home_win REAL,
                    draw REAL,
                    away_win REAL,
                    description TEXT,
                    match_id integer,
                    FOREIGN KEY(match_id) REFERENCES match_table(id));'''

drop_odds_table = "DROP TABLE IF EXISTS odds_table;"
