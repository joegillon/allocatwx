from collections import namedtuple

EmployeeMatch = namedtuple('EmployeeMatch', 'id names')


class Employee(object):

    def __init__(self, d):
        self.name = d['name']
        self.grade = d['grade']
        self.step = d['step']
        self.fte = d['fte']
        self.investigator = d['investigator']
        self.notes = d['notes']

    @staticmethod
    def get_all(dao):
        sql = "SELECT * FROM employees ORDER BY name;"
        rex = dao.execute(sql)
        return {rec['id']: rec for rec in rex} if rex else {}

    @staticmethod
    def get_all_active(dao):
        sql = ("SELECT * FROM employees "
               "WHERE active=1 "
               "ORDER BY name;")
        rex = dao.execute(sql)
        return {rec['id']: rec for rec in rex} if rex else {}

    @staticmethod
    def get_investigators(dao):
        sql = ("SELECT * FROM employees "
               "WHERE investigator=1 "
               "ORDER BY name;")
        return dao.execute(sql)

    @staticmethod
    def get_one(dao, empId):
        sql = "SELECT * FROM employees WHERE id=?"
        return dao.execute(sql, (empId,))[0]

    @staticmethod
    def getAsns(dao, empid, month=None):
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
        return dao.execute(sql, vals)

    @staticmethod
    def add(dao, d):
        d['active'] = 1
        sql = "INSERT INTO employees (%s) VALUES (%s);" % (
            ','.join(d.keys()), '?' + ',?' * (len(d) - 1)
        )
        vals = list(d.values())
        return dao.execute(sql, vals)

    @staticmethod
    def update(dao, emp, d):
        if emp['name'].upper() == d['name'].upper():
            del d['name']
        sql = ("UPDATE employees "
               "SET %s "
               "WHERE id=?;") % (
            ','.join(f + '=?' for f in d.keys()))
        vals = list(d.values()) + [emp['id']]
        return dao.execute(sql, vals)

    @staticmethod
    def delete(dao, ids):
        sql = "DELETE FROM employees WHERE id IN (%s);" % \
              ','.join(['?'] * len(ids))
        return dao.execute(sql, ids)
