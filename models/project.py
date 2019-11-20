from models.dao import Dao


class Project(object):
    def __init__(self, name, nickname, first_month, last_month, notes):
        self.name = name
        self.nickname = nickname
        self.first_month = first_month
        self.last_month = last_month
        self.notes = notes

    @staticmethod
    def get_all():
        sql = "SELECT * FROM projects ORDER BY nickname;"
        return Dao.execute(sql)

    @staticmethod
    def get_all_active():
        sql = ("SELECT * FROM projects "
               "WHERE active=1 "
               "ORDER BY nickname;")
        return Dao.execute(sql)

    @staticmethod
    def getAsns(prjid, month=None):
        sql = ("SELECT a.id AS id, "
               "a.employee_id AS employee_id, "
               "a.first_month AS first_month, "
               "a.last_month AS last_month, "
               "a.effort AS effort, "
               "a.notes AS notes, "
               "e.name AS employee "
               "FROM assignments AS a "
               "JOIN employees AS e ON a.employee_id= e.id "
               "WHERE a.project_id=? "
               "AND a.active=1 ")
        vals = [prjid]
        if month:
            sql += "AND a.last_month >= ? "
            vals += [month]
        sql += "ORDER BY e.name;"
        return Dao.execute(sql, vals)

    @staticmethod
    def add(d):
        del d['id']
        sql = "INSERT INTO projects (%s) VALUES (%s);" % (
            ','.join(d.keys()), '?' + ',?' * (len(d) - 1)
        )
        vals = list(d.values())
        return Dao.execute(sql, vals)

    @staticmethod
    def update(d):
        prjid = d['id']
        del d['id']
        sql = ("UPDATE projects "
               "SET %s "
               "WHERE id=?;") % (
            ','.join(f + '=?' for f in d.keys()))
        vals = list(d.values()) + [prjid]
        return Dao.execute(sql, vals)

    @staticmethod
    def delete(ids):
        sql = "DELETE FROM projects WHERE id IN (%s);" % \
              ','.join(['?'] * len(ids))
        return Dao.execute(sql, ids)

    @staticmethod
    def update_pi(prjid, empid):
        sql = ("UPDATE projects "
               "SET principal_investigator=? "
               "WHERE id=?;")
        vals = (empid, prjid)
        return Dao.execute(sql, vals)
