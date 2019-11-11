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
               "WHERE a.employee_id=? ")
        vals = [empid]
        if month:
            sql += "AND a.last_month >= ? "
            vals += [month]
        sql += "ORDER BY p.nickname;"
        return Dao.execute(sql, vals)
