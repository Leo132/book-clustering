from enum import Enum
from pydantic import BaseModel

# for web
class Page(str, Enum):
    login = "login"
    register = "register"
    index = "index"
    collections = "collections"

class LoginInfo(BaseModel):
    username: str
    password: str

class RegisterInfo(BaseModel):
    name: str
    username: str
    password: str
    password_confirm: str

# for database
class Table(str, Enum):
    books = "books"
    authors = "authors"
    phouses = "phouses"
    clusters = "clusters"
    users = "users"
    writing = "writing"
    collections = "collections"
