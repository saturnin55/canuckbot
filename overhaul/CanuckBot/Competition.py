from pydantic import HttpUrl
from datetime import date
from . import CanuckBotBase
from .types import Handle, HexColor, SnowflakeId
from .Competition_Type import Competition_Type


class Competition(CanuckBotBase):
    competition_id: int
    name: str
    shortname = Handle
    logo_url: HttpUrl
    color = HexColor
    competition_type: Competition_Type
    is_monitored: bool
    is_international: bool
    optout_role_id = SnowflakeId
    category_id = SnowflakeId
    hours_before_kickoff: int
    hours_after_kickoff: int
    created_at: date
