'''
Database access functions lib
'''
import pymysql
try:
    from lib.datatype import Table      # if running ./src/main.py
except ImportError:
    from datatype import Table          # if running ./src/lib/db_f.py

_DATABASE = "book_clustering"

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
        return conn
    except Exception as e:
        print("Error: database connecting fail...")
        print(e)

def _init_db(conn):
    with open("./src/init.sql", 'r', encoding="utf-8") as f:
        for query in f.read().split("\n\n"):
            _query(conn, query)

# for authors, phouses, clusters
def _load_data(conn, data: list[dict]):
    for table, infos in data.items():
        for info in infos:
            _insert_row(conn, table, list(info.keys()), list(info.values()))

# only for books
def _load_book_info(conn, book_infos: list[dict]):
    for idx, book_info in enumerate(book_infos, start=1):
        # author_id is a multi-value attribute
        original_keys = ["book_name", "ISBN13", "category", "published_date", "price", "pages"]
        foreign_keys = ["phouse_id", "cluster_id"]

        # original info (list[str]) + foreign info (list[str])
        cols = original_keys + foreign_keys
        vals = [book_info[key] for key in original_keys] + [
            _search_cols(conn, "phouses", ["phouse_id"], [f'phouse_name = "{book_info["phouse"]}"'])[0]["phouse_id"],
            book_info["cluster"],
        ]
        # print(cols)
        # print(vals)
        _insert_row(conn, "books", cols, vals)
        # print("finish book insert")

        # author info (insert to `writing` table)
        cols = ["ISBN13", "author_id"]
        for author_name in book_info["author"]:
            vals = [
                book_info["ISBN13"],
                _search_cols(conn, "authors", ["author_id"], [f'author_name = "{author_name}"'])[0]["author_id"],
            ]
            _insert_row(conn, "writing", cols, vals)
        # print(f"{idx:3d}. inserted")

def _query(conn, query_str: str, have_result: bool=False):
    # print(f"{query_str=}")        # for debugging

    with conn.cursor() as cursor:
        cursor.execute(query_str)

        if have_result:
            return cursor.description, cursor.fetchall()

    conn.commit()

def _create_table_if_not_exists(conn, table: Table, data: list[str]):
    query = f"create table if not exists {table} ({', '.join(data)});"

    _query(conn, query)

def _search(conn, query: str, cols: list[str]=None):
    descriptions, rows = _query(conn, query, True)

    if not cols:
        cols = [desc[0] for desc in descriptions]

    return [{col : r for col, r in zip(cols, row)} for row in rows]

def _search_cols(conn, table: Table, cols: list[str]=None, conditions: list[str]=None):
    query = f"select {', '.join(cols) if cols else '*'} from {table}{' where ' + ' and '.join(conditions) if conditions else ''};"

    return _search(conn, query, cols)

def _search_foreign_cols(conn, table: Table, ref_table: Table, fk: str, pk: str, cols: list[str]=None, conditions: list[str]=None):
    query = f"select {', '.join(cols) if cols else '*'} from {table} inner join {ref_table} on {table}.{fk} = {ref_table}.{pk}{' where ' + ' and '.join(conditions) if conditions else ''};"

    return _search(conn, query, cols)

def _insert_row(conn, table: Table, cols: list[str], vals: list[str]):
    vals = list(map(lambda val: f'"{val}"' if isinstance(val, str) else str(val), vals))
    query = f"insert into {table} ({', '.join(cols)}) values ({', '.join(vals)});"

    _query(conn, query)

def _delete_row(conn, table: Table, conditions: list[str]):
    query = f"delete from {table}{' where ' + ' and '.join(conditions) if conditions else ''};"

    _query(conn, query)

def get_books(cols: list[str]=None, conditions: list[str]=None):
    with _connect_db(_DATABASE) as conn:
        query = "SELECT books.ISBN13, phouse_name, phouses.phouse_id, book_name, category, published_date, pages, price FROM books " +  \
                "INNER JOIN phouses ON phouses.phouse_id = books.phouse_id " +                                                          \
                f"WHERE {' and '.join(conditions)}" if conditions else ''
        descriptions, rows = _query(conn, query, True)
        cols = [desc[0] for desc in descriptions] + ["author_name"]
        result = [{col : r for col, r in zip(cols, row)} for row in rows]
        for book_info in result:
            query = "SELECT author_name FROM authors " +                                 \
                    "INNER JOIN writing ON authors.author_id = writing.author_id " +     \
                    f"WHERE ISBN13 = '{book_info['ISBN13']}'"
            _, author_name = _query(conn, query, True)
            book_info["author_name"] = [d[0] for d in author_name]

    return result

def get_authors(cols: list[str], conditions: list[str]):
    with _connect_db(_DATABASE) as conn:
        result = _search_foreign_cols(conn, "authors", "writing", "author_id", "author_id", cols, conditions)
    return result

def get_phouses(cols: list[str], conditions: list[str]):
    with _connect_db(_DATABASE) as conn:
        result = _search_foreign_cols(conn, "phouses", "books", "phouse_id", "phouse_id", cols, conditions)
    return result

def get_clusters(cols: list[str], conditions: list[str]):
    with _connect_db(_DATABASE) as conn:
        result = _search_cols(conn, "clusters", cols, conditions)
    return result

def get_collections(cols: list[str], conditions: list[str]):
    with _connect_db(_DATABASE) as conn:
        query = "SELECT collections.ISBN13, phouses.phouse_name, book_name, category, published_date, pages, price FROM collections " + \
                "INNER JOIN books ON collections.ISBN13 = books.ISBN13 " +                                                              \
                "INNER JOIN phouses ON books.phouse_id = phouses.phouse_id " +                                                          \
                f"WHERE {' and '.join(conditions)}" if conditions else ''
        descriptions, rows = _query(conn, query, True)
        cols = [desc[0] for desc in descriptions] + ["author_name"]
        result = [{col : r for col, r in zip(cols, row)} for row in rows]
        for book_info in result:
            query = "SELECT author_name FROM authors " +                                 \
                    "INNER JOIN writing ON authors.author_id = writing.author_id " +     \
                    f"WHERE ISBN13 = '{book_info['ISBN13']}'"
            _, author_name = _query(conn, query, True)
            book_info["author_name"] = [d[0] for d in author_name]
    return result

# return True if exists
def _username_check(conn, username: str):
    user_info = _search_cols(conn, "users", ["user_id", "name"], [f"username = '{username}'"])
    return len(user_info) > 0, user_info

def _password_check(conn, password: str):
     user_info = _search_cols(conn, "users", ["user_id", "name"], [f"password = '{password}'"])
     return len(user_info) > 0

def _name_check(conn, name: str):
    user_info = _search_cols(conn, "users", ["user_id", "name"], [f"name = '{name}'"])
    return len(user_info) > 0

async def login_check(username: str, password: str):
    with _connect_db(_DATABASE) as conn:
        (username_check, user_info), password_check = _username_check(conn, username), _password_check(conn, password)
    return  {
        "is_username_exist": username_check,
        "is_password_correct": password_check,
        "user_info": user_info if not username_check else user_info[0],
    }

async def register_check(name: str, username: str, password: str, password_confirm: str):
    with _connect_db(_DATABASE) as conn:
        name_check, (username_check, _) = _name_check(conn, name), _username_check(conn, username)
        if not name_check and not username_check and password == password_confirm:
            _insert_row(conn, "users", ["name", "username", "password"], [name, username, password])
    return  {
        "is_name_exist": name_check,
        "is_username_exist": username_check,
    }

async def collect_book(user_id: int, ISBN13: str):
    with _connect_db(_DATABASE) as conn:
        _insert_row(conn, "collections", ["user_id", "ISBN13"], [user_id, ISBN13])

async def remove_book(user_id: int, ISBN13: str):
    with _connect_db(_DATABASE) as conn:
        _delete_row(conn, "collections", [f"user_id = {user_id}", f"ISBN13 = '{ISBN13}'"])

def _init(*, reset_db: bool=False, load_data: bool=False):
    with _connect_db(_DATABASE) as conn:
        if reset_db:
            _query(conn, "drop database if exists book_clustering")
            _init_db(conn)

        if load_data:
            from utils import load_json
            data = {f"{d}s": load_json(f"./data/{d}_info.json") for d in ["author", "phouse", "cluster"]}
            _load_data(conn, data)
            _load_book_info(conn, load_json("./data/book_info.json"))

def _test():
    # _init(reset_db=False, load_data=False)
    conn = _connect_db(_DATABASE)
    for row in _search_cols(conn, "books")[:5]:
        print(row)

if __name__ == "__main__":
    # _test()
    _init(reset_db=True, load_data=True)
else:
    _init()