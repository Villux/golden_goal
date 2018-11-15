import json
import requests
from functools import partial
import pandas as pd
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count

from db import player_identity_table as pit
from logger import logging

def has_goalcom_url(fifa_id, conn):
    pit_data = pit.get_by_fifa_id(fifa_id, conn=conn)
    if pit_data.shape[0] == 0:
        logging.warning(f"No player for id {fifa_id}")
        return False
    else:
        if pit_data["goalcom_name"].item():
            return True
        return False

def is_url_mapped_to_player(goalcom_url, conn):
    fifa_id = pit.get_id_by_goalcom_url(goalcom_url, conn=conn)
    if fifa_id:
        return True
    return False

def get_team_history_from_page(page_text):
    data = []

    bs = BeautifulSoup(page_text, 'html.parser')

    table = bs.find("table", {"class": "real-career"})
    if table:
        table_body = table.find('tbody')

        rows = table_body.findAll('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

        season_object = {}
        for row in data:
            if len(row) > 1:
                season_object[row[0]] = row[1]
        return season_object
    else:
        return {}

def player_squad_history(fifa_id):
    page = requests.get(f"https://sofifa.com/player/{fifa_id}/live", timeout=10)
    return get_team_history_from_page(page.text)

def add_team_by_date(player, date):
    year = int(date[0:4])
    month = int(date[5:7])

    if month < 7:
        season_tag = f"{year-1}/{year}"
    else:
        season_tag = f"{year}/{year+1}"

    season_object = player_squad_history(player["id"])
    player["team"] = season_object.get(season_tag, None)
    return player

def get_player_suggestions(name, date):
    url = f"https://sofifa.com/ajax.php?action=playerSuggestion&gender=0&hl=en-US&term={name}"
    headers = {
        'content-type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        "Referer": "https://sofifa.com/players/hot"
    }
    page = requests.get(url, headers=headers, timeout=10)
    player_list = page.json()
    if player_list[0]["name"] == "No Result Found":
        player_list = []

    pool = Pool(cpu_count() * 2)
    player_list = pool.map(partial(add_team_by_date, date=date), player_list)
    pool.close()
    return player_list


def map_player_manually(player, last_name, conn):
    player_list = get_player_suggestions(last_name, player["date"])

    for idx, fifa_player in enumerate(sorted(player_list, key=lambda k: k['fullname'], reverse=False)):
        already_fifa_id = has_goalcom_url(fifa_player["id"], conn)
        print(f"[{idx}] {fifa_player['fullname']} {already_fifa_id} {fifa_player['team']} {fifa_player['overall']}")

    user_input = input(f"\nMatching for {player['name']} {player['url_id']} {player['team']}: \n")
    if user_input:
        return {
            'fifa_id': int(player_list[int(user_input)]["id"]),
            'goalcom_name': player["name"],
            "goalcom_url": player["url_id"]
        }
    return {}
