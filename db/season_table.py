from db import helper as dbh
from db.interface import fetchone, fetchall

table_name = "season_table"

def insert(division_id, description, start_date, end_date, **kwargs):
    data = {
        "division_id": division_id,
        "description": description,
        "start_date": start_date,
        "end_date": end_date
    }
    return dbh.insert(table_name, kwargs["conn"], **data)

def get_previous_season(season_id, **kwargs):
    conn = kwargs["conn"]

    start_date_query = f"select start_date, division_id from season_table where id={season_id};"
    (start_date, division_id) = fetchone(start_date_query, conn)

    query = f"select id from season_table where end_date < '{start_date}' and division_id={division_id} order by end_date desc;"
    return fetchone(query, conn)

def get_seasons_for_division(division, **kwargs):
    if not division:
        query = f"select id from season_table;"
    elif isinstance(division, list):
        query = f"select id from season_table where division_id IN ({','.join(str(idd) for idd in division)});"
    elif isinstance(division, int):
        query = f"select id from season_table where division_id={division};"

    return fetchall(query, kwargs["conn"])
