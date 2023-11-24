from typing import Any
from enum import Enum

class Page(str, Enum):
    login = "login"
    register = "register"
    index = "index"