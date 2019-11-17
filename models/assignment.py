from models.dao import Dao
from utils.strutils import monthUglify


class Assignment(object):
    def __init__(self, empId, prjId, firstMonth, lastMonth, effort, notes):
        self.empId = empId
        self.prjId = prjId
        self.firstMonth = firstMonth
        self.lastMonth = lastMonth
        self.effort = effort
        self.notes = notes

    @staticmethod
    def getOne(asnId):
        sql = "SELECT * FROM assignments WHERE id=?"
        vals = [asnId]
        return Dao.execute(sql, vals)

    @staticmethod
    def get_for_timeframe(first_month, last_month):
        sql = ("SELECT a.id AS id, "
               "a.employee_id AS employee_id, "
               "a.project_id AS project_id, "
               "a.first_month AS first_month, "
               "a.last_month AS last_month, "
               "a.effort AS effort, "
               "e.name AS employee, "
               "p.nickname AS project "
               "FROM assignments AS a "
               "JOIN employees AS e ON a.employee_id=e.id "
               "JOIN projects AS p ON a.project_id=p.id "
               "WHERE a.first_month >= ? AND a.last_month <= ?")
        vals = (monthUglify(first_month), monthUglify(last_month))
        return Dao.execute(sql, vals)
