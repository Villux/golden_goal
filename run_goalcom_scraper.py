import time
import argparse
import pandas as pd
import goalcom.scraper as goalcom

parser = argparse.ArgumentParser()
parser.add_argument('-d', type=str)
args = parser.parse_args()

def read_dates(filename="match_dates.csv"):
    date_df = pd.read_csv(filename)
    return date_df.Date.values

dates = read_dates()

query_dates = []
for date in dates:
    if time.strptime(date, "%Y-%m-%d") >= time.strptime(args.d, "%Y-%m-%d"):
        query_dates.append(date)

goalcom.run(query_dates)
