#
# just a script to import data from the old canuckbot
#
import json
import sqlite3

DB_PATH = '../database/database.db'  # Path to your SQLite database

def read_config(file):
   try:
      with open(file) as infile:
         data = json.load(infile)
   except Exception as e:
      print("ERR2(read_config): {0}".format(e))

   return(data)

teams = read_config("teams.json")

db = sqlite3.connect(DB_PATH)
cursor = db.cursor()

for key, value in teams.items():
   handle = teams[key]['discord_name']
   tz = teams[key]['tz']
   
   cursor.execute('INSERT INTO teams (name, tz) VALUES (?, ?)', (key, tz))
   id_team = cursor.lastrowid

   if "aliases" in teams[key].keys():
      aliases = teams[key]["aliases"]
      for alias in teams[key]["aliases"]:
         #print(f"{key} => alias: {alias}")
         cursor.execute('INSERT INTO team_aliases (id_team, alias) VALUES (?, ?)', (id_team, alias))

db.commit()
cursor.close()
