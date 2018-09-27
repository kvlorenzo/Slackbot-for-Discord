import sqlite3


class Schema:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.c = self.conn.cursor()

    def create_tables(self):
        members_table = """
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_id INTEGER,
            channel_id INTEGER,
            user_id INTEGER
        )
        """

        responses_table = """
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_added INTEGER,
            member_id INTEGER,
            message TEXT,
            response TEXT
        )
        """

        reminders_table = """
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            date_added INTEGER,
            recipient_type TEXT,
            recipient_id INTEGER,
            message TEXT,
            send_time INTEGER
        )
        """
        self.c.execute(members_table)
        self.c.execute(responses_table)
        self.c.execute(reminders_table)

    def close_db(self):
        self.conn.commit()
        self.conn.close()
