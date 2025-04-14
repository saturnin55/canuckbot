from typing import Any
from .constants import *
#from CanuckBot import Info
from .utils import timestamp2str, get_discord_user, key_value_exists, get_discord_channel, get_discord_category, is_valid_type, get_field_value, regex_is_integer, pp_discord_channel, pp_discord_category, pp_hex_color, pp_discord_role, get_discord_role, pp_discord_user, pp_timestamp, pp_url, pp_bool, pp_string, pp_int, get_type_name, is_snowflakeid

__all__ = ["timestamp2str", "get_discord_user", "get_discord_channel", "key_value_exists", "get_discord_category", "is_valid_type", "CanuckBotBase","get_field_value","regex_is_integer", "pp_discord_channel", "pp_discord_category", "pp_hex_color", "pp_discord_role", "get_discord_role", "pp_discord_user", "pp_timestamp", "pp_url", "pp_bool", "pp_string", "pp_int", "get_type_name", "is_snowflakeid" ]

class CanuckBotBase:
    obj = None
    FIELDS = {}

    def __init__(self, bot):
        self.bot = bot
        self.database = bot.database

    def val(field: str, flag_raw: bool = True) -> Any:
        pass 

    def get_field_type(self, field: str) -> Any:
        if self.field_exists(field):
            return self.FIELDS[field]["type"]
        else:
            return False

    def field_exists(self, field: str) -> Any:
        if field in self.FIELDS:
            return True
        else:
            return False

    def load_data(self, row):
        if not row:
            return False

        for key, value in row.items():
            _type = self.get_field_type(key)
            print(f"{key}|{_type}|{value}|")

            if not is_valid_type(_type, value):
                print(f"ERR: wrong type ({_type}) {self.obj}.{key} = |{value}|")
                return False

            if value is None:
                self.data[key] = None
                return True

            if _type in [ TYPE_INT, TYPE_DISCORD_USERID, TYPE_DISCORD_CHANNELID, TYPE_DISCORD_CATEGORYID, TYPE_DISCORD_ROLEID, TYPE_DISCORD_MESSAGEID]:
                self.data[key] = int(value)
            elif _type == TYPE_BOOL:
                self.data[key] = bool(value)
            elif _type in [ TYPE_STRING, TYPE_URL, TYPE_COLOR]:
                self.data[key] = str(value)
            elif _type == TYPE_TIMESTAMP:
                self.data[key] = int(value)
            else:
                print(f"ERR: can't load field {self.obj}.{key} = |{value}|")

        return True

    #async def get_field_info(self, field=None) -> str:
         
        #else:
        #    return "—"

    #async def set_field_info(self, obj: str = None, field=None, value:str = None) -> bool:
    #    pass
    def print(self):
        print(f"{self.obj:<12}:")
        print("=============")
        for f in self.FIELDS:
            t = self.FIELDS[f]['type']
            _type = get_type_name(self.FIELDS[f]['type'])
            v = self.get(f)
            if not v:
                print(f"   {f:<15} {_type:<15} : |—|")
            else:
                print(f"   {f:<15} {_type:<15} : |{v}|")
