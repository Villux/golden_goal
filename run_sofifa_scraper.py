import time
import argparse
import sofifa.scraper as sofifa

parser = argparse.ArgumentParser()
parser.add_argument('-d', type=str)
args = parser.parse_args()

date_filter = None
if args.d:
    date_filter = time.strptime(args.d, "%Y-%m-%d")

sofifa.run(date_filter)
