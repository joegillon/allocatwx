import sqlite3
import globals as gbl


class Dao(object):
    def __init__(self, stateful=None, db=None):
        if db:
            self.__db = db
        else:
            self.__db = sqlite3.connect(gbl.DB_PATH)

        # This is so project and employee deletes will also drop
        # their assignments
        self.__db.execute('PRAGMA FOREIGN_KEYS = ON')

        self.__cursor = self.__db.cursor()
        self.__sql = ''
        self.__params = []
        self.__stateful = stateful

    def execute(self, sql, params=None):
        self.__sql = sql
        self.__params = params
        op = self.__sql.split(' ', 1)[0].upper()
        if op == 'SELECT':
            result = self.__read()
        else:
            self.__write()
            if op == 'INSERT':
                return self.__cursor.lastrowid
            else:
                return self.__cursor.rowcount
        if not self.__stateful:
            self.__db.close()
        return result

    def __read(self):
        # Seems you can't pass a None type to the execute func.
        if self.__params:
            n = self.__cursor.execute(self.__sql, self.__params)
        else:
            n = self.__cursor.execute(self.__sql)
        if not n:
            return []
        rex = self.__cursor.fetchall()
        flds = [f[0] for f in self.__cursor.description]
        return [dict(zip(flds, rec)) for rec in rex] if rex else []

    def __write(self):
        self.__cursor.execute(self.__sql, self.__params)
        self.__db.commit()

    def close(self):
        self.__db.close()
