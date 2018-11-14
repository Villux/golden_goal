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

create_lineup_table = '''CREATE TABLE lineup_table
                    (id integer PRIMARY KEY AUTOINCREMENT,
                    url text,
                    hp1 integer,
                    hp2 integer,
                    hp3 integer,
                    hp4 integer,
                    hp5 integer,
                    hp6 integer,
                    hp7 integer,
                    hp8 integer,
                    hp9 integer,
                    hp10 integer,
                    hp11 integer,
                    hs1 integer,
                    hs2 integer,
                    hs3 integer,
                    hs4 integer,
                    hs5 integer,
                    hs6 integer,
                    hs7 integer,
                    ap1 integer,
                    ap2 integer,
                    ap3 integer,
                    ap4 integer,
                    ap5 integer,
                    ap6 integer,
                    ap7 integer,
                    ap8 integer,
                    ap9 integer,
                    ap10 integer,
                    ap11 integer,
                    as1 integer,
                    as2 integer,
                    as3 integer,
                    as4 integer,
                    as5 integer,
                    as6 integer,
                    as7 integer,
                    match_id integer UNIQUE,
                    FOREIGN KEY(hp1) REFERENCES player_identity_table(id),
                    FOREIGN KEY(hp2) REFERENCES player_identity_table(id),
                    FOREIGN KEY(hp3) REFERENCES player_identity_table(id),
                    FOREIGN KEY(hp4) REFERENCES player_identity_table(id),
                    FOREIGN KEY(hp5) REFERENCES player_identity_table(id),
                    FOREIGN KEY(hp6) REFERENCES player_identity_table(id),
                    FOREIGN KEY(hp7) REFERENCES player_identity_table(id),
                    FOREIGN KEY(hp8) REFERENCES player_identity_table(id),
                    FOREIGN KEY(hp9) REFERENCES player_identity_table(id),
                    FOREIGN KEY(hp10) REFERENCES player_identity_table(id),
                    FOREIGN KEY(hp11) REFERENCES player_identity_table(id),
                    FOREIGN KEY(hs1) REFERENCES player_identity_table(id),
                    FOREIGN KEY(hs2) REFERENCES player_identity_table(id),
                    FOREIGN KEY(hs3) REFERENCES player_identity_table(id),
                    FOREIGN KEY(hs4) REFERENCES player_identity_table(id),
                    FOREIGN KEY(hs5) REFERENCES player_identity_table(id),
                    FOREIGN KEY(hs6) REFERENCES player_identity_table(id),
                    FOREIGN KEY(hs7) REFERENCES player_identity_table(id),
                    FOREIGN KEY(ap1) REFERENCES player_identity_table(id),
                    FOREIGN KEY(ap2) REFERENCES player_identity_table(id),
                    FOREIGN KEY(ap3) REFERENCES player_identity_table(id),
                    FOREIGN KEY(ap4) REFERENCES player_identity_table(id),
                    FOREIGN KEY(ap5) REFERENCES player_identity_table(id),
                    FOREIGN KEY(ap6) REFERENCES player_identity_table(id),
                    FOREIGN KEY(ap7) REFERENCES player_identity_table(id),
                    FOREIGN KEY(ap8) REFERENCES player_identity_table(id),
                    FOREIGN KEY(ap9) REFERENCES player_identity_table(id),
                    FOREIGN KEY(ap10) REFERENCES player_identity_table(id),
                    FOREIGN KEY(ap11) REFERENCES player_identity_table(id),
                    FOREIGN KEY(as1) REFERENCES player_identity_table(id),
                    FOREIGN KEY(as2) REFERENCES player_identity_table(id),
                    FOREIGN KEY(as3) REFERENCES player_identity_table(id),
                    FOREIGN KEY(as4) REFERENCES player_identity_table(id),
                    FOREIGN KEY(as5) REFERENCES player_identity_table(id),
                    FOREIGN KEY(as6) REFERENCES player_identity_table(id),
                    FOREIGN KEY(as7) REFERENCES player_identity_table(id),
                    FOREIGN KEY(match_id) REFERENCES match_table(id));'''

drop_lineup_table = "DROP TABLE IF EXISTS lineup_table;"

create_match_id_index = "CREATE INDEX match_id_index ON lineup_table (match_id);"

create_player_identity_table = '''CREATE TABLE player_identity_table
                    (fifa_name text,
                    goalcom_name text,
                    fifa_id INTEGER PRIMARY KEY,
                    goalcom_url text);'''

drop_player_identity_table = "DROP TABLE IF EXISTS player_identity_table;"

create_fifa_id_index = "CREATE INDEX pit_fifa_id_index ON player_identity_table (fifa_id);"
