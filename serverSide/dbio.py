"""database io implement."""
import sqlite3

SQL_CREATE_TABLE = "CREATE TABLE IF NOT EXISTS \
    myIP(id INTEGER PRIMARY KEY AUTOINCREMENT \
    ,hostname TEXT, uid TEXT, ip TEXT, status INTEGER \
    , updateTime TEXT, info TEXT)"

SQL_SELECT_ALL = "SELECT * FROM myIP ORDER BY updateTime DESC"

SQL_SELECT_ONE = "SELECT * FROM myIP WHERE hostname=? order by updateTime DESC"

SQL_INSERT = "INSERT INTO myIP(hostname, uid, ip, status, updateTime, info)\
    values(?,?,?,?,?,?)"

SQL_UPDATE = "UPDATE myIP SET ip = ?, status = ?,updateTime = ?,info = ? \
    WHERE hostname = ? AND uid = ?"

SQL_DELETE = "DELETE FROM myIP WHERE hostname = ?"
SQL_DELETE_ALL = "DELETE FROM myIP"
DEFAULT_DB_NAME = 'test.db'


class DBIO():

    def __init__(self, db_name=DEFAULT_DB_NAME):
        """
        docstring here
            :param db_name="test.db":
        """
        print('init_func')
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        # cur = self.conn.cursor()
        # cur.execute(SQL_CREATE_TABLE)
        # self.conn.commit()
        with self.conn:
            self.conn.execute(SQL_CREATE_TABLE)
        self.conn.close()

    def __call__(self):
        print('I\'m in the function')

    def __enter__(self, db_name=DEFAULT_DB_NAME):
        self.conn = sqlite3.connect(db_name)
        return self.conn

    def __exit__(self, exception_type, exception_value, traceback):
        self.conn.close()

    def __get_conn(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __close_conn(self):
        self.conn.close()


def add(hostname, uid, ip, status, updateTime, info):
    t = (hostname, uid, ip, status, updateTime, info)
    with DBIO() as conn:
        with conn:
            conn.execute(SQL_INSERT, t)


def update(hostname, uid, ip, status, updateTime, info):
    t = (ip, status, updateTime, info, hostname, uid)
    with DBIO() as conn:
        with conn:
            conn.execute(SQL_UPDATE, t)


def get(hostname):
    t = (hostname,)
    with DBIO() as conn:
        with conn:
            return [i for i in conn.execute(SQL_SELECT_ONE, t)]


def getAll():
    with DBIO() as conn:
        with conn:
            return [i for i in conn.execute(SQL_SELECT_ALL)]


def delAll():
    with DBIO() as conn:
        with conn:
            conn.execute(SQL_DELETE_ALL)


def delete(hostname):
    t = (hostname, )
    with DBIO() as conn:
        with conn:
            conn.execute(SQL_DELETE, t)


if __name__ == "__main__":
    test = DBIO()
    add('myName', '23', '234,', 342, '2018-10-27', 'info')
    print(get('myName', '23'))
