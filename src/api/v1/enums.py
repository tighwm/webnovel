from enum import Enum


class Action(Enum):
    READ = "read"
    CREATE = "create"
    EDIT = "edit"
    DELETE = "delete"


class Resource(Enum):
    NOVEL = "novel"
    USER = "user"
