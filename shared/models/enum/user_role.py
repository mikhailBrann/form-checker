from enum import Enum as PyEnum


class UserRole(PyEnum):
    admin  = "admin"
    master = "master"
    user   = "user"