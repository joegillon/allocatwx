from models.dao import Dao


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
