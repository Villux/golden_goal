import time
import json
from multiprocessing import Pool, cpu_count
import requests
from bs4 import BeautifulSoup

from logger import get_logger
from goalcom.parser import get_match_links_for_league, get_lineup

def add_lineup_to_match_link(links):
    modified_links = []
    for link in links:
        start, end = link.rsplit('/', 1)
        modified_links.append(start + "/lineups/" + end)
    return modified_links

def get_lineup_for_match(match_link):
    page = requests.get(url + match_link)
    bs = BeautifulSoup(page.text, 'html.parser')
    lineup = get_lineup(bs)
    lineup["match_url_id"] = match_link
    bs.decompose()
    return lineup

logging = get_logger()

number_of_cores = cpu_count() * 4
url = "https://www.goal.com/"
league_id = "2kwbbcootiqqgmrzs6o5inle5"

def run(dates):
    logging.debug(f'Got {len(dates)} dates')

    for date in dates:
        logging.info(f"Starting to scrape matches {date}")

        page = requests.get(url + "en/results/" + date)

        bs = BeautifulSoup(page.text, 'html.parser')
        match_links = add_lineup_to_match_link(get_match_links_for_league(bs, league_id))
        bs.decompose()

        pool = Pool(number_of_cores)
        results = pool.map(get_lineup_for_match, match_links)
        pool.close()

        for data_obj in results:
            data_obj["date"] = date

        with open(f'lineups/data_{date}.json', 'w') as outfile:
            json.dump(results, outfile)
