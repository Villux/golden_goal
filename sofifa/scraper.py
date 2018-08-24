from multiprocessing import Pool, cpu_count
import numpy as np
import pandas as pd

from sofifa.utils import get_page, build_url, RedirectException
from sofifa.parser import get_data_update_query_strings, parse_player_data
from services import player
from logger import get_logger
from db.interface import open_connection, close_connection

def get_player_data(url):
    try:
        bs = get_page(url)
        return parse_player_data(bs)
    except RedirectException:
        return False

logging = get_logger()

number_of_cores = cpu_count()
players_per_page = 50

player_url = "https://sofifa.com/players"

def run():
    conn = open_connection()
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

            player.insert_or_update_player_data(df, date, conn=conn)
            conn.commit()

            offset = offset_list[-1]
    close_connection(conn)

if __name__ == "__main__":
    run()