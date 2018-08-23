create_elo_table = '''CREATE TABLE elo_table
                    (id integer PRIMARY KEY AUTOINCREMENT,
                    date text, team text, elo real,
                    match_id integer,
                    FOREIGN KEY(match_id) REFERENCES match_table(id));'''

drop_elo_table = "DROP TABLE IF EXISTS elo_table;"
