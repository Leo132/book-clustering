from typing import Any
from enum import Enum

# for web
class Page(str, Enum):
    login = "login"
    register = "register"
    index = "index"

# for database
class Table(str, Enum):
    books = "books"
    authors = "authors"
    phouses = "phouses"
    clusters = "clusters"
    users = "users"
    writing = "writing"
    collections = "collections"