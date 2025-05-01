from enum import IntEnum


class User_Level(IntEnum):
    Superadmin = 0
    Full = 10
    Trusted = 20
    Public = 99
