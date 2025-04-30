from datetime import date
from typing import List

from . import CanuckBotBase
from .types import SnowflakeId
from .User_Level import User_Level


class Manager(CanuckBotBase):
    user_id = SnowflakeId
    created_at: date
    created_by = SnowflakeId
    level: User_Level
    competitions: List[int]
