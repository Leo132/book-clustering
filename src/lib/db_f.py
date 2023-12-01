'''
Database access functions lib
'''
import pymysql

def connect_db(db_settings: dict):
    try:
        conn = pymysql.connect(**db_settings)
        print("database connect successful!")
        return conn
    except Exception as e:
        print(e)

def _query(conn, query_str, result=False):
    print(query_str)        # for debug

    with conn.cursor() as cursor:
        cursor.execute(query_str)

        if result:
            return (cursor.description, cursor.fetchall())

    conn.commit()

def _create_table_if_not_exists(conn, table, data):
    sql_query = f"create table if not exists {table} ({', '.join(data)});"

    _query(conn, sql_query)

def _search_cols(conn, table, cols=None, conditions=None):
    sql_query = f"select {', '.join(cols) if cols else '*'} from {table}{' where ' + conditions if conditions else ''};"

    description, rows = _query(conn, sql_query, True)

    if not cols:
        cols = [description[i][0] for i in range(len(description))]

    return [{cols[i] : row[i] for i in range(len(cols))} for row in rows]

def _insert_row(conn, table, cols, vals):
    sql_query = f"insert into {table} ({', '.join(cols)}) values ({', '.join(vals)});"

    _query(conn, sql_query)

def insert_book_info(conn, book_info):
    pass

def search_book_by_key(conn, key):
    pass


def _test():
    pass

if __name__ == "__main__":
    _test()