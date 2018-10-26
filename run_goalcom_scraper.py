import time
import argparse
import pandas as pd
import goalcom.scraper as goalcom

def read_dates(filename="match_dates.csv"):
    date_df = pd.read_csv(filename)
    return date_df.Date.values

dates = read_dates()
goalcom.run(dates)
