import sqlite3

from database import query


class Entry:
    # Constructor initializes the Entry class by connecting to the server
    # database and instantiating the member dict. The member_dict variable is a
    # dictionary with a setup as such:
    # member_dict = {
    #         "server_id": ctx.message.server.id
    #         "channel_id": ctx.message.channel.id,
    #         "user_id": ctx.message.author.id
    # }
    def __init__(self, db, member_dict):
        self.db = db
        self.conn = sqlite3.connect(db)
        self.c = self.conn.cursor()
        self.member_dict = member_dict

    def add_response(self, msg, response):
        member_id = query.Query(self.db)

    def add_member(self):
        with self.conn:
            self.c.execute("INSERT INTO members VALUES "
                           "(null, :server_id, :channel_id, :user_id)",
                           self.member_dict)
            self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()
