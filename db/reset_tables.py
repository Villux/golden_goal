from db import player_queries as pq
from db.interface import execute_statement, open_connection, close_connection

if __name__ == "__main__":
    conn = open_connection()
    execute_statement(pq.drop_query, conn)
    execute_statement(pq.create_query, conn)
    execute_statement(pq.create_index, conn)
    close_connection(conn)