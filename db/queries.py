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
                    p1 integer,
                    p2 integer,
                    p3 integer,
                    p4 integer,
                    p5 integer,
                    p6 integer,
                    p7 integer,
                    p8 integer,
                    p9 integer,
                    p10 integer,
                    p11 integer,
                    s1 integer,
                    s2 integer,
                    s3 integer,
                    s4 integer,
                    s5 integer,
                    s6 integer,
                    s7 integer,
                    match_id integer,
                    FOREIGN KEY(p1) REFERENCES player_identity_table(id),
                    FOREIGN KEY(p2) REFERENCES player_identity_table(id),
                    FOREIGN KEY(p3) REFERENCES player_identity_table(id),
                    FOREIGN KEY(p4) REFERENCES player_identity_table(id),
                    FOREIGN KEY(p5) REFERENCES player_identity_table(id),
                    FOREIGN KEY(p6) REFERENCES player_identity_table(id),
                    FOREIGN KEY(p7) REFERENCES player_identity_table(id),
                    FOREIGN KEY(p8) REFERENCES player_identity_table(id),
                    FOREIGN KEY(p9) REFERENCES player_identity_table(id),
                    FOREIGN KEY(p10) REFERENCES player_identity_table(id),
                    FOREIGN KEY(p11) REFERENCES player_identity_table(id),
                    FOREIGN KEY(s1) REFERENCES player_identity_table(id),
                    FOREIGN KEY(s2) REFERENCES player_identity_table(id),
                    FOREIGN KEY(s3) REFERENCES player_identity_table(id),
                    FOREIGN KEY(s4) REFERENCES player_identity_table(id),
                    FOREIGN KEY(s5) REFERENCES player_identity_table(id),
                    FOREIGN KEY(s6) REFERENCES player_identity_table(id),
                    FOREIGN KEY(s7) REFERENCES player_identity_table(id),
                    FOREIGN KEY(match_id) REFERENCES match_table(id));'''

drop_lineup_table = "DROP TABLE IF EXISTS lineup_table;"

create_player_identity_table = '''CREATE TABLE player_identity_table
                    (id integer PRIMARY KEY AUTOINCREMENT,
                    fifa_name text,
                    goalcom_name text,
                    fifa_id INTEGER,
                    goalcom_url text);'''

drop_player_identity_table = "DROP TABLE IF EXISTS player_identity_table;"
