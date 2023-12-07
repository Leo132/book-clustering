'''
Database access functions lib
'''
import pymysql


def _connect_db(database: str=None):
    import os
    from dotenv import load_dotenv

    try:
        dotenv_path = "./.env"
        load_dotenv(dotenv_path, override=True)
        db_settings = {
            "host" : "localhost",
            "port" : 3306,
            "user": os.getenv("DB_USER"),
            "password" : os.getenv("DB_PASSWORD"),
            "database": database,
            "charset" : "utf8",
        }
        conn = pymysql.connect(**db_settings)
        print("database connect successful!")
        return conn
    except Exception as e:
        print("Error: database connecting fail...")
        print(e)

def _init_db(conn, load_data: bool=False):
    with open("./src/init.sql", 'r', encoding="utf-8") as f:
        for query in f.read().split("\n\n"):
            _query(conn, query)

# for authors, phouses, clusters
def _load_data(conn, data: list[dict]):
    for table, infos in data.items():
        for info in infos:
            _insert_row(conn, table, list(info.keys()), list(info.values()))
    # for testing
    _query(conn, "INSERT INTO `clusters`(`book_num`, `average_price`, `average_pages`, `average_time`) VALUES (10, 250, 300, 123)")

# only for books
def _load_book_info(conn, book_infos: list[dict]):
    for idx, book_info in enumerate(book_infos, start=1):
        # author_id is a multi-value attribute
        original_keys = ["name", "ISBN13", "category", "published_date", "price", "pages"]
        foreign_keys = ["phouse_id", "cluster_id"]

        # original info (list[str]) + foreign info (list[str])
        cols = original_keys + foreign_keys
        vals = [book_info[key] for key in original_keys] + [
            _search_cols(conn, "phouses", ["phouse_id"], [f"name = '{book_info['phouse']}'"])[0]["phouse_id"],
            book_info["cluster"],
        ]
        print(cols)
        print(vals)
        _insert_row(conn, "books", cols, vals)
        print("finish book insert")

        # author info (insert to `writing` table)
        cols = ["ISBN13", "author_id"]
        for author_name in book_info["author"]:
            vals = [
                book_info["ISBN13"],
                _search_cols(conn, "authors", ["author_id"], [f"name = '{author_name}'"])[0]["author_id"],
            ]
            _insert_row(conn, "writing", cols, vals)
        print(f"{idx:3d}. inserted")

def _query(conn, query_str: str, have_result: bool=False):
    # print(query_str)        # for debugging

    with conn.cursor() as cursor:
        cursor.execute(query_str)

        if have_result:
            return cursor.description, cursor.fetchall()

    conn.commit()

def _create_table_if_not_exists(conn, table: str, data: list[str]):
    query = f"create table if not exists {table} ({', '.join(data)});"

    _query(conn, query)

def _search(conn, query: str, cols: list[str]=None):
    description, rows = _query(conn, query, True)

    if not cols:
        cols = [description[i][0] for i in range(len(description))]

    return [{cols[i] : row[i] for i in range(len(cols))} for row in rows]

def _search_cols(conn, table: str, cols: list[str]=None, conditions: list[str]=None):
    query = f"select {', '.join(cols) if cols else '*'} from {table}{' where ' + ' and '.join(conditions) if conditions else ''};"
    print(query)

    return _search(conn, query, cols)

def _search_foreign_cols(conn, table: str, ref_table: str, fk: str, pk: str, cols: list[str]=None):
    query = f"select {', '.join(cols) if cols else '*'} from {table} inner join {ref_table} on {table}.{fk} = {ref_table}.{pk};"

    return _search(conn, query, cols)

def _insert_row(conn, table: str, cols: list[str], vals: list[str]):
    vals = list(map(lambda val: f'"{val}"' if isinstance(val, str) else str(val), vals))
    # cols = list(map(lambda col: f"`{col}`", cols))
    # print(cols)
    query = f"insert into {table} ({', '.join(cols)}) values ({', '.join(vals)});"
    print(query)

    _query(conn, query)


def _init(*, reset_db: bool=False, load_data: bool=False):
    conn = _connect_db()
    if reset_db:
        _query(conn, "drop database if exists book_clustering")

    _init_db(conn)

    if load_data:
        from utils import load_json
        data = {f"{d}s": load_json(f"./data/{d}_info.json") for d in ["author", "phouse", "cluster"]}
        _load_data(conn, data)
        # _load_book_info(conn, load_json("./data/book_info.json"))

def _test():
    _init(reset_db=True, load_data=True)

if __name__ == "__main__":
    _test()
else:
    _init()