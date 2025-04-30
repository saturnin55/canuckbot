from enum import IntEnum


class User_Level(IntEnum):
    Superadmin = 0
    Full = 1
    Trusted = 2
    Public = 99
