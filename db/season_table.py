from db import helper as dbh
from db.interface import fetchone

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
