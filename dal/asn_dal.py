import lib.month_lib as ml


def get_all(dao):
    sql = "SELECT * FROM assignments;"
    return dao.execute(sql)


def get_one(dao, asnId):
    sql = "SELECT * FROM assignments WHERE id=?"
    vals = [asnId]
    return dao.execute(sql, vals)


def get_for_timeframe(dao, first_month, last_month):
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
    vals = (ml.uglify(first_month), ml.uglify(last_month))
    return dao.execute(sql, vals)


def add(dao, d):
    d['active'] = 1
    sql = "INSERT INTO assignments (%s) VALUES (%s);" % (
        ','.join(d.keys()), '?' + ',?' * (len(d) - 1)
    )
    vals = list(d.values())
    return dao.execute(sql, vals)


def update(dao, asnId, d):
    sql = ("UPDATE assignments "
           "SET %s "
           "WHERE id=?;") % (
        ','.join(f + '=?' for f in d.keys()))
    vals = list(d.values()) + [asnId]
    return dao.execute(sql, vals)


def delete(dao, ids):
    sql = "DELETE FROM assignments WHERE id IN (%s);" % \
          ','.join(['?'] * len(ids))
    return dao.execute(sql, ids)
