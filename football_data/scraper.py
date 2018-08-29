import pandas as pd
import numpy as np
import requests

from logger import logging
from services import match
from db.interface import open_connection, close_connection
from db import division_table as dt
from db import season_table as st

url = "http://www.football-data.co.uk/mmz4281/"

years_tags = ["0001", "0102", "0203", "0304", "0405", "0506", "0607",
              "0708", "0809", "0910", "1011", "1112", "1213", "1314",
              "1415", "1516", "1617", "1718"]

def read_csv(address):
    dirty_df = pd.read_csv(address, names=list(range(300)))
    columns = dirty_df.iloc[0].dropna().values
    df = dirty_df.iloc[1:, :len(columns)]
    columns = [col.replace('>', 'gt') for col in columns]
    columns = [col.replace('<', 'lt') for col in columns]
    columns = [col.replace('.', '') for col in columns]
    df.columns = columns
    df = df.rename(columns={
        'HS': 'Home_Team_Shots',
        'AS': 'Away_Team_Shots',
        'HG': 'FTHG',
        'AG': 'FTAG',
        'Res': 'FTR',
        'PH': 'PSH',
        'PD': 'PSD',
        'PA': 'PSA'})

    if len(df["Date"].iloc[0]) > 8:
        df["Date"] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    else:
        df["Date"] = pd.to_datetime(df['Date'], format='%d/%m/%y')

    df["Date"] = df["Date"].dt.strftime('%Y-%m-%d')
    return df

def run():
    conn = open_connection()

    div_ids = dt.insert_divisions_by_tags(dt.ENGLAND, conn=conn)
    data_tags = dt.get_tags_for_ids(div_ids, conn=conn)

    for year_tag in years_tags:
        logging.info(f"Reading football data for year tag {year_tag}")

        for division_id, division_tag in zip(div_ids, data_tags):
            csv_url = f"{url}{year_tag}/{division_tag}.csv"
            try:
                df = read_csv(csv_url)
            except UnicodeDecodeError:
                logging.warning(f"Failed to read csv for year tag {year_tag}")
                page = requests.get(csv_url)
                csv_file = page.text.encode().decode("utf-8")
                with open("tmp.csv", "w") as f:
                    f.write(csv_file)
                df = read_csv("tmp.csv")

            df = df.dropna(thresh=10)
            start_date = df["Date"].replace(["NaN", 'NaT'], np.nan).dropna().min()
            end_date = df["Date"].replace(["NaN", 'NaT'], np.nan).dropna().max()
            st_id = st.insert(division_id, year_tag, start_date, end_date, conn=conn)
            match.insert_matches(df, st_id, conn=conn)
            conn.commit()
    close_connection(conn)

if __name__ == "__main__":
    run()
