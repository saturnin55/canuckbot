from enum import IntEnum


class Competition_Type(IntEnum):
    Men = 0
    Women = 1

    def __str__(self):
        return self.name
