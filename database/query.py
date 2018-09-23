import sqlite3


class Query:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.c = self.conn.cursor()

    def get_member_id(self, member_dict):
        self.c.execute("SELECT id from members WHERE server_id = :server_id "
                       "AND channel_id = :channel_id AND user_id = :user_id",
                       member_dict)
        data = self.c.fetchall()
        if len(data) < 1:
            return None
        return data[0][0]

    def get_msg_response(self, server_id, msg):
        self.c.execute("SELECT response FROM responses WHERE member_id IN "
                       "(SELECT id from members WHERE server_id = ?)"
                       " AND message = ? COLLATE NOCASE",
                       (server_id, msg))
        response = self.c.fetchall()
        if len(response) < 1:
            return None
        return response[0][0]

    def get_all_responses(self, server_id):
        self.c.execute("SELECT message, response FROM responses WHERE "
                       "member_id IN "
                       "(SELECT id from members WHERE server_id = ?)",
                       (server_id,))
        return self.c.fetchall()

    def close(self):
        self.conn.commit()
        self.conn.close()
