import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cur = self.conn.cursor()

    def create_user(self, chat_id):
        self.cur.execute("""insert into weathers(user_id) values (?)""", (chat_id,))
        self.conn.commit()

    def get_user_by_chat_id(self, chat_id):
        self.cur.execute("""select * from weathers where user_id = ?""", (chat_id, ))
        user = dict_fetchone(self.cur)
        return user

    def get_user_by_id(self):
        self.cur.execute("""select user_id from weathers""")
        user_id = dict_fetchall(self.cur)
        return user_id

def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def dict_fetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))