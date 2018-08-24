create_query = '''
    CREATE TABLE IF NOT EXISTS "match_table" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "Div" TEXT,
        "Date" TIMESTAMP,
        "HomeTeam" TEXT,
        "AwayTeam" TEXT,
        "FTHG" INTEGER,
        "FTAG" INTEGER,
        "FTR" TEXT,
        "HTHG" INTEGER,
        "HTAG" INTEGER,
        "HTR" TEXT,
        "Referee" TEXT,
        "Home_Team_Shots" INTEGER,
        "Away_Team_Shots" INTEGER,
        "HST" INTEGER,
        "AST" INTEGER,
        "HF" INTEGER,
        "AF" INTEGER,
        "HC" INTEGER,
        "AC" INTEGER,
        "HY" INTEGER,
        "AY" INTEGER,
        "HR" INTEGER,
        "AR" INTEGER,
        "Attendance" TEXT,
        "HHW" INTEGER,
        "AHW" INTEGER,
        "HO" INTEGER,
        "AO" INTEGER,
        "HBP" INTEGER,
        "ABP" INTEGER,
        CONSTRAINT UC_match UNIQUE (HomeTeam,AwayTeam,Date)
    );
'''

create_index = "CREATE INDEX match_index ON match_table (id);"

drop_query = "DROP TABLE IF EXISTS match_table;"
