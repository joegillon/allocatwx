import sqlite3


def getDB():
    cxn = sqlite3.connect(':memory:')
    c = cxn.cursor()

    sql = ("CREATE TABLE projects ("
           "id INTEGER PRIMARY KEY NOT NULL,"
           "name TEXT NOT NULL UNIQUE,"
           "nickname TEXT NOT NULL UNIQUE,"
           "notes TEXT DEFAULT (NULL),"
           "first_month TEXT NOT NULL,"
           "last_month TEXT NOT NULL,"
           "PI INTEGER REFERENCES employees (id),"
           "PM INTEGER REFERENCES employees (id),"
           "active BOOLEAN DEFAULT (1));")
    c.execute(sql)

    sql = ("CREATE TABLE employees ("
           "id INTEGER PRIMARY KEY NOT NULL,"
           "name TEXT NOT NULL UNIQUE,"
           "grade INTEGER,"
           "step INTEGER,"
           "fte INTEGER,"
           "notes TEXT,"
           "investigator BOOLEAN DEFAULT (0),"
           "active BOOLEAN DEFAULT (1));")
    c.execute(sql)

    sql = ("CREATE TABLE assignments ("
           "id INTEGER PRIMARY KEY NOT NULL,"
           "employee_id INTEGER NOT NULL "
           "REFERENCES employees (id) ON DELETE CASCADE,"
           "project_id INTEGER NOT NULL "
           "REFERENCES projects (id) ON DELETE CASCADE,"
           "first_month TEXT NOT NULL,"
           "last_month TEXT NOT NULL,"
           "effort INTEGER,"
           "notes TEXT,"
           "active BOOLEAN DEFAULT (1));")
    c.execute(sql)

    cxn.commit()
    return cxn
