import numpy as np

from db.interface import execute_statement, fetchone

insert_query = 'insert into {table_name} ({columns}) values ({placeholders})'

def guarantee_python_types(obj):
    if isinstance(obj, np.generic):
        return np.asscalar(obj)
    return obj

def get_value_tuple(row):
    values = [guarantee_python_types(value) for value in row.values()]
    return tuple(values)

def build_insert_query(data, table_name):
    columns = data.keys()
    placeholders = ["?"] * len(columns)
    query = insert_query.format(table_name=table_name, columns=','.join(columns),placeholders=','.join(placeholders))
    return query

def build_update_query_set(data):
    elements = []
    for key, _ in data.items():
        elements.append(f'{key}=?')
    return ','.join(elements)

def insert(table_name, conn, **kwargs):
    query = build_insert_query(kwargs, table_name)
    values = get_value_tuple(kwargs)
    execute_statement((query, values), conn)
    return fetchone("select last_insert_rowid()", conn)[0]
