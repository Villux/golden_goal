
from multiprocessing import Pool, cpu_count
import pandas as pd

from db.interface import open_connection, close_connection
import db.match_table as mt
from services import data_provider
from logger import logging

conn = open_connection()

def get_feature_vector_for_match(match):
    match_df = mt.get_match(match["id"], conn=conn)
    feature_vector = {}
    if match_df.shape[0]:
        match_data = match_df.iloc[0, :].to_dict()
        feature_vector = {**match_data, **data_provider.create_match_feature_vector(match_data, conn=conn)}
    else:
        logging.warning(f"No match data for match id {match['id']}")
    return feature_vector

def run():
    pool = Pool(cpu_count() * 3)
    match_df = mt.get_matches_for_division(1, "2006-01-01", conn=conn)
    matches = [record for (_, record) in match_df.to_dict('index').items()]
    match_features = pool.map(get_feature_vector_for_match, matches)
    df = pd.DataFrame(match_features)
    df.to_csv("new_master_data.csv")
    pool.close()


if __name__ == "__main__":
    run()
    close_connection(conn)