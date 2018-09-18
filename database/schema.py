import sqlite3

conn = sqlite3.connect("server.db")
c = conn.cursor()

members_table = """
CREATE TABLE members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    server_id INTEGER,
    channel id INTEGER,
    user_id INTEGER
)
"""

responses_table = """
CREATE TABLE responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_added INTEGER,
    member_id INTEGER,
    message TEXT,
    response TEXT
)
"""

reminders_table = """
CREATE TABLE reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_added INTEGER,
    member_author_id INTEGER,
    member_receiver_id INTEGER,
    receiver_type TEXT,
    message TEXT,
    send_time INTEGER
)
"""
c.execute(members_table)
c.execute(responses_table)
c.execute(reminders_table)

conn.commit()
conn.close()
