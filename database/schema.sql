CREATE TABLE IF NOT EXISTS team_aliases (
id_team INTEGER,
alias TEXT
);
CREATE TABLE IF NOT EXISTS teams (
id_team INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
   tz TEXT default "American/Toronto",
handle TEXT DEFAULT NULL
);
CREATE TABLE IF NOT EXISTS competitions (
id_competition INTEGER PRIMARY KEY AUTOINCREMENT,
handle TEXT NOT NULL,
flag_active BOOLEAN default TRUE,
name TEXT default NULL,
logo TEXT default NULL,
create_before INTEGER default 24,
delete_after INTEGER default 24,
color TEXT default NULL,
roleid_optout TEXT default NULL,
category TEXT default NULL,
flag_intl BOOLEAN default 0);
CREATE TABLE IF NOT EXISTS matches (
id_match INTEGER PRIMARY KEY AUTOINCREMENT,
home INTEGER NOT NULL,
away INTEGER NOT NULL,
id_competition INTEGER NOT NULL,
status TEXT default '',
dt_kickoff timestamp DEFAULT NULL,
dt_delete timestamp DEFAULT  NULL,
tz TEXT NOT NULL,
venue TEXT NOT NULL,
description TEXT default NULL,
channel_name TEXT default NULL,
channel_id TEXT default NULL,
flag_warned BOOLEAN default FALSE,
channel_topic TEXT default NULL,
msgid_welcome TEXT default NULL,
hours_before INTEGER default NULL,
hours_after INTEGER default NULL,
_key TEXT default NULL);
CREATE TABLE IF NOT EXISTS info (
 id_info INTEGER PRIMARY KEY AUTOINCREMENT,
 obj TEXT NOT NULL,
 field TEXT NOT NULL,
 info TEXT DEFAULT NULL
 );
CREATE TABLE IF NOT EXISTS managers (
userid INTEGER NOT NULL PRIMARY KEY,
dt_added timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
added_by INTEGER DEFAULT NULL
);
CREATE TABLE IF NOT EXISTS config (field TEXT PRIMARY KEY NOT NULL, value TEXT);
