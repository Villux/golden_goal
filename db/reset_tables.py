from db import player_queries as pq
from db import match_queries as mq
from db import queries as q
from db.interface import execute_statement, open_connection, close_connection

if __name__ == "__main__":
    conn = open_connection()
    # execute_statement(pq.drop_query, conn)
    # execute_statement(pq.create_query, conn)
    # execute_statement(pq.create_index, conn)

    execute_statement(mq.drop_query, conn)
    execute_statement(mq.create_query, conn)
    execute_statement(mq.create_index, conn)

    execute_statement(q.drop_odds_table, conn)
    execute_statement(q.create_odds_table, conn)

    execute_statement(q.drop_division_table, conn)
    execute_statement(q.create_division_table, conn)

    execute_statement(q.drop_season_table, conn)
    execute_statement(q.create_season_table, conn)

    execute_statement(q.drop_elo_table, conn)
    execute_statement(q.create_elo_table, conn)


    close_connection(conn)
