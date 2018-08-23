from db.interface import execute_statement, fetchall
from db.helper import get_value_tuple, build_insert_query, build_update_query_set

table_name = 'player_table'

def insert(conn, **kwargs):
    query = build_insert_query(kwargs, table_name)
    values = get_value_tuple(kwargs)
    execute_statement((query, values), conn)
    return execute_statement("select last_insert_rowid()", conn)

def update_by_id(fifa_id, conn, **kwargs):
    set_text = build_update_query_set(kwargs)
    query = f"UPDATE player_table SET {set_text} WHERE fifa_id={fifa_id};"
    execute_statement((query, get_value_tuple(kwargs)), conn)

def get_existing_indexes(indexes, date, conn):
    id_list = ','.join(str(x) for x in indexes)
    query = f"select fifa_id from player_table where fifa_id in ({id_list}) and date='{date}';"
    existing_idx = fetchall(query, conn)
    return [idx[0] for idx in existing_idx]
