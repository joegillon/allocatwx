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
               "a.employee_id AS employee_id, "
               "a.first_month AS first_month, "
               "a.last_month AS last_month, "
               "a.effort AS effort, "
               "a.notes AS notes, "
               "e.name AS employee "
               "FROM assignments AS a "
               "JOIN employees AS e ON a.employee_id= e.id "
               "WHERE a.project_id=? ")
        vals = [prjid]
        if month:
            sql += "AND a.last_month >= ? "
            vals += [month]
        sql += "ORDER BY e.name;"
        return Dao.execute(sql, vals)
