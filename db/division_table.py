from db import helper as dbh
from db.interface import fetchall

table_name = "division_table"

ENGLAND = [("E0", "Premier League"), ("E1", "Championship"), ("E2", "League 1"), ("E3", "League 2")]

def insert(conn, **kwargs):
    return dbh.insert(table_name, conn, **kwargs)

def insert_divisions_by_tags(tags, **kwargs):
    conn = kwargs["conn"]
    ids = []
    for tag, description in tags:
        data = {
            "data_tag" : tag,
            "description": description
        }
        div_id = insert(conn, **data)
        ids.append(div_id)
    return ids

def get_tags_for_ids(ids, **kwargs):
    conn = kwargs["conn"]
    query = f"select data_tag from division_table where id IN ({','.join(str(idd) for idd in ids)})"
    ret = fetchall(query, conn)
    return [val[0] for val in ret]
