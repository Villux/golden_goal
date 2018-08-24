create_elo_table = '''CREATE TABLE elo_table
                    (id integer PRIMARY KEY AUTOINCREMENT,
                    date TIMESTAMP,
                    team text,
                    elo real,
                    match_id integer,
                    season_id INTEGER NOT NULL,
                    FOREIGN KEY(season_id) REFERENCES season_table(id),
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

create_division_table = '''CREATE TABLE division_table
                    (id integer PRIMARY KEY AUTOINCREMENT,
                    data_tag text,
                    description text);'''

drop_division_table = "DROP TABLE IF EXISTS division_table;"

create_season_table = '''CREATE TABLE season_table
                    (id integer PRIMARY KEY AUTOINCREMENT,
                    start_date TIMESTAMP,
                    end_date TIMESTAMP,
                    description text,
                    division_id INTEGER,
                    FOREIGN KEY(division_id) REFERENCES division_table(id));'''

drop_season_table = "DROP TABLE IF EXISTS season_table;"
