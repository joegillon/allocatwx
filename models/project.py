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
               "WHERE a.project_id=? ")
        vals = [prjid]
        if month:
            sql += "AND a.last_month >= ? "
            vals += [month]
        sql += "ORDER BY e.name;"
        return Dao.execute(sql, vals)
