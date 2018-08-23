import argparse
import logging
from multiprocessing import Pool, cpu_count
import numpy as np
import pandas as pd

from sofifa.utils import get_page, build_url, RedirectException
from sofifa.parser import get_data_update_query_strings, parse_player_data
from db.interface import open_connection, close_connection
from db import player_table as pt
from services import player

def get_player_data(url):
    try:
        bs = get_page(url)
        return parse_player_data(bs)
    except RedirectException:
        return False

formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("scraper.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logging.basicConfig(
    format=formatter,
    level=logging.DEBUG,
    handlers=[
        stream_handler,
        file_handler
    ])

number_of_cores = cpu_count()
players_per_page = 50

player_url = "https://sofifa.com/players"

def run():
    bs = get_page(player_url)
    dates = get_data_update_query_strings(bs)
    logging.debug(f'Got {len(dates)} dates')
    bs.decompose()

    for date, query_string in dates.items():
        logging.info(f"Starting to scrape data for {query_string}")

        offset = 0

        wip = True
        while wip:
            end_offset = offset + number_of_cores * players_per_page
            offset_list = np.arange(offset, end_offset, players_per_page)
            urls = [build_url(player_url, query_string, offset_val) for offset_val in offset_list]

            pool = Pool(cpu_count())
            results = pool.map(get_player_data, urls)
            pool.close()

            if False in results:
                wip = False

            results = [result for result in results if result != False]
            results = [item for sublist in results for item in sublist]
            df = pd.DataFrame(results)
            df["date"] = date
            df["query_string"] = query_string
            df = df.set_index("fifa_id")

            player.insert_or_update_player_data(df)

            offset = offset_list[-1]

if __name__ == "__main__":
    run()