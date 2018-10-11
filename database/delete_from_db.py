import sqlite3

from database import query


class Deletion:
    def __init__(self, db):
        self.db = db
        self.query = query.Query(self.db)
        self.conn = sqlite3.connect(db)
        self.c = self.conn.cursor()

    def del_msg(self, server_id, msg):
        # Uses query to check if the message exists in the database
        if self.query.get_msg_response(server_id, msg) is None:
            return False
        self.c.execute("DELETE FROM responses WHERE member_id IN "
                       "(SELECT id from members WHERE server_id = ?)"
                       " AND message = ? COLLATE NOCASE",
                       (server_id, msg))
        self.conn.commit()
        return True

    def del_response(self, server_id, response):
        # Checks first if the response exists in the database
        self.c.execute("SELECT * FROM responses WHERE member_id IN "
                       "(SELECT id from members WHERE server_id = ?)"
                       " AND response = ? COLLATE NOCASE",
                       (server_id, response))
        result = self.c.fetchall()
        if len(result) < 1:
            return False
        self.c.execute("DELETE FROM responses WHERE member_id IN "
                       "(SELECT id from members WHERE server_id = ?)"
                       " AND response = ? COLLATE NOCASE",
                       (server_id, response))
        self.conn.commit()
        return True

    def del_all_responses(self, server_id):
        # Checks responses exist in the database
        self.c.execute("SELECT * FROM responses WHERE member_id IN "
                       "(SELECT id from members WHERE server_id = ?)",
                       (server_id,))
        result = self.c.fetchall()
        if len(result) < 1:
            return False
        self.c.execute("DELETE FROM responses WHERE member_id IN "
                       "(SELECT id from members WHERE server_id = ?)",
                       (server_id,))
        self.conn.commit()
        return True

    def del_reminder(self, server_id, reminder):
        self.c.execute("SELECT * FROM reminders WHERE member_id IN "
                       "(SELECT id from members WHERE server_id = ?)"
                       " AND message = ? COLLATE NOCASE",
                       (server_id, reminder))
        result = self.c.fetchall()
        if len(result) < 1:
            return False
        self.c.execute("DELETE FROM reminders WHERE member_id IN "
                       "(SELECT id from members WHERE server_id = ?)"
                       " AND response = ? COLLATE NOCASE",
                       (server_id, reminder))
        self.conn.commit()
        return True

    def del_all_reminders(self, server_id):
        # Checks responses exist in the database
        self.c.execute("SELECT * FROM reminders WHERE member_id IN "
                       "(SELECT id from members WHERE server_id = ?)",
                       (server_id,))
        result = self.c.fetchall()
        if len(result) < 1:
            return False
        self.c.execute("DELETE FROM reminders WHERE member_id IN "
                       "(SELECT id from members WHERE server_id = ?)",
                       (server_id,))
        self.conn.commit()
        return True

    def close(self):
        self.conn.commit()
        self.conn.close()
