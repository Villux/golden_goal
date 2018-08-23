from db.interface import execute_statement, fetchone
from db.helper import get_value_tuple, build_insert_query

table_name = "elo_table"

def insert(conn, **kwargs):
    query = build_insert_query(kwargs, table_name)
    values = get_value_tuple(kwargs)
    execute_statement((query, values), conn)
    return execute_statement("select last_insert_rowid()", conn)

def select_latest_for_team(team, date, conn):
    query = 'SELECT elo, id FROM elo_table WHERE team=? AND date < ? ORDER BY date DESC;'
    return fetchone((query, (team,date)), conn)[0]

def attach_match_to_elo(match_id, id_a, id_b, conn):
    query = f"update elo_table set match_id=? where id=?;"
    execute_statement((query, (match_id, id_a)), conn)
    execute_statement((query, (match_id, id_b)), conn)
