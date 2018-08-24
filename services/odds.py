from db import odds_table as ot
from db.interface import open_connection, close_connection

bookmakers = {
    "Avg": "Oddsportal Average",
    "B365" : "Bet365",
    "BS": "Blue Square",
    "BW": "Bet&Win",
    "GB": "Gamebookers",
    "IW": "Interwetten",
    "LB": "Ladbroker",
    "SO": "Sporting Odds",
    "SB": "Sportingbet",
    "SJ": "Stan James",
    "SY": "Stanleybet",
    "VC": "VC Bet",
    "WH": "William Hill",
    "PSC": "Pinnacle closing",
    "PS": "Pinnacle",
    "P": "Pinnacle",
    "BbAv": "Bookbeat average"
}

def insert_odds_for_match(record, match_id, conn):
    odds = []

    for key, value in bookmakers.items():
        home_odd = record.get(key + "H", None)
        draw_odd = record.get(key + "D", None)
        away_odd = record.get(key + "A", None)

        if home_odd and draw_odd and away_odd:
            odds.append({
                "description": value,
                "home_win": float(home_odd),
                "draw": float(draw_odd),
                "away_win": float(away_odd),
                "match_id": match_id
            })
    for odd in odds:
        ot.insert(conn, **odd)
