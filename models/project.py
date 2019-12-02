from collections import namedtuple

ProjectMatch = namedtuple('ProjectMatch', 'id values' )


class Project(object):

    @staticmethod
    def get_all(dao):
        sql = "SELECT * FROM projects ORDER BY nickname;"
        rex = dao.execute(sql)
        return {rec['id']: rec for rec in rex} if rex else {}

    @staticmethod
    def get_all_active(dao):
        sql = ("SELECT * FROM projects "
               "WHERE active=1 "
               "ORDER BY nickname;")
        rex = dao.execute(sql)
        return {rec['id']: rec for rec in rex} if rex else {}

    @staticmethod
    def get_one(dao, prjId):
        sql = "SELECT * FROM projects WHERE id=?"
        return dao.execute(sql, (prjId,))[0]

    @staticmethod
    def get_by_name(dao, name):
        sql = "SELECT * FROM projects WHERE name=?"
        return dao.execute(sql, (name,))[0]

    @staticmethod
    def get_by_nickname(dao, nickname):
        sql = "SELECT * FROM projects WHERE nickname=?"
        return dao.execute(sql, (nickname,))[0]

    @staticmethod
    def getAsns(dao, prjid, month=None):
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
               # "AND a.active=1 ")
        vals = [prjid]
        if month:
            sql += "AND a.last_month >= ? "
            vals += [month]
        sql += "ORDER BY e.name;"
        return dao.execute(sql, vals)

    @staticmethod
    def add(dao, d):
        d['active'] = 1
        d['PI'] = None
        d['PM'] = None
        sql = "INSERT INTO projects (%s) VALUES (%s);" % (
            ','.join(d.keys()), '?' + ',?' * (len(d) - 1)
        )
        vals = list(d.values())
        try:
            return dao.execute(sql, vals)
        except Exception as e:
            if str(e) == 'UNIQUE constraint failed: projects.nickname':
                raise Exception('Project nickname is not unique!')
            else:
                raise

    @staticmethod
    def update(dao, prj, d):
        if prj['name'].upper() == d['name'].upper():
            del d['name']
        if prj['nickname'].upper() == d['nickname'].upper():
            del d['nickname']
        sql = ("UPDATE projects "
               "SET %s "
               "WHERE id=?;") % (
            ','.join(f + '=?' for f in d.keys()))
        vals = list(d.values()) + [prj['id']]
        return dao.execute(sql, vals)

    @staticmethod
    def delete(dao, ids):
        sql = "DELETE FROM projects WHERE id IN (%s);" % \
              ','.join(['?'] * len(ids))
        return dao.execute(sql, ids)

    @staticmethod
    def update_pi(dao, prjid, empid):
        sql = ("UPDATE projects "
               "SET principal_investigator=? "
               "WHERE id=?;")
        vals = (empid, prjid)
        return dao.execute(sql, vals)
