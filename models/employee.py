from models.dao import Dao


class Employee(object):
    def __init__(self, name, grade, step, fte, notes, investigator):
        self.name = name
        self.grade = grade
        self.step = step
        self.fte = fte
        self.notes = notes
        self.investigator = investigator

    @staticmethod
    def get_all():
        sql = "SELECT * FROM employees ORDER BY name;"
        rex = Dao.execute(sql)
        return {rec['id']: rec for rec in rex} if rex else {}

    @staticmethod
    def get_all_active():
        sql = ("SELECT * FROM employees "
               "WHERE active=1 "
               "ORDER BY name;")
        rex = Dao.execute(sql)
        return {rec['id']: rec for rec in rex} if rex else {}

    @staticmethod
    def get_investigators():
        sql = ("SELECT * FROM employees "
               "WHERE investigator=1 "
               "ORDER BY name;")
        return Dao.execute(sql)

    @staticmethod
    def getAsns(empid, month=None):
        sql = ("SELECT a.id AS id, "
               "a.project_id AS project_id, "
               "a.first_month AS first_month, "
               "a.last_month AS last_month, "
               "a.effort AS effort, "
               "a.notes AS notes, "
               "p.nickname AS project "
               "FROM assignments AS a "
               "JOIN projects AS p ON a.project_id= p.id "
               "WHERE a.employee_id=? "
               "AND a.active=1 ")
        vals = [empid]
        if month:
            sql += "AND a.last_month >= ? "
            vals += [month]
        sql += "ORDER BY p.nickname;"
        return Dao.execute(sql, vals)

    @staticmethod
    def add(d):
        del d['id']
        sql = "INSERT INTO employees (%s) VALUES (%s);" % (
            ','.join(d.keys()), '?' + ',?' * (len(d) - 1)
        )
        vals = list(d.values())
        return Dao.execute(sql, vals)

    @staticmethod
    def update(d):
        empid = d['id']
        del d['id']
        sql = ("UPDATE employees "
               "SET %s "
               "WHERE id=?;") % (
            ','.join(f + '=?' for f in d.keys()))
        vals = list(d.values()) + [empid]
        return Dao.execute(sql, vals)

    @staticmethod
    def delete(ids):
        sql = "DELETE FROM employees WHERE id IN (%s);" % \
              ','.join(['?'] * len(ids))
        return Dao.execute(sql, ids)
