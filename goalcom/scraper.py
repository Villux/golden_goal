import time
import json
from multiprocessing import Pool, cpu_count
import requests
from bs4 import BeautifulSoup

from logger import get_logger
from goalcom.parser import get_match_links_for_league, get_lineup

TIMEOUT = 10

match_ids = []

def add_lineup_to_match_link(links):
    modified_links = []
    for link in links:
        start, match_id = link.rsplit('/', 1)
        modified_links.append([start + "/lineups/", match_id])
    return modified_links

def get_lineup_for_match(args):
    match_link, match_id = args
    logging.debug(f"Requesting page {url}{match_link}{match_id}")
    page = requests.get(url + match_link + match_id, timeout=TIMEOUT)
    bs = BeautifulSoup(page.text, 'html.parser')
    lineup = get_lineup(bs)
    lineup["match_id"] = match_id
    bs.decompose()
    return lineup

logging = get_logger()

number_of_cores = cpu_count() * 4
url = "https://www.goal.com"
league_id = "2kwbbcootiqqgmrzs6o5inle5"

pool = Pool(number_of_cores)

def run(dates):
    logging.debug(f'Got {len(dates)} dates')

    for date in dates:
        logging.info(f"Starting to scrape matches {url}/en/results/{date}")

        page = requests.get(url + "/en/results/" + date, timeout=TIMEOUT)

        bs = BeautifulSoup(page.text, 'html.parser')
        match_links = add_lineup_to_match_link(get_match_links_for_league(bs, league_id))
        bs.decompose()

        valid_links = []
        for match_url, match_id in match_links:
            if match_id not in match_ids:
                valid_links.append([match_url, match_id])

        results = pool.map(get_lineup_for_match, valid_links)

        for data_obj in results:
            data_obj["date"] = date

        with open(f'lineups/data_{date}.json', 'w') as outfile:
            json.dump(results, outfile)

        for _, match_id in valid_links:
            match_ids.append(match_id)

    pool.close()