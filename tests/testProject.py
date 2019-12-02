import unittest
from tests.setup_db import getDB
from models.dao import Dao
from models.project import Project
from models.employee import Employee
from models.assignment import Assignment

mockDB = getDB()


class TestProject(unittest.TestCase):
    # def setUp(self):
    #     self.prj = None
    #     self.formData = {}

    def testAdd(self):
        dao = Dao(stateful=True, db=mockDB)

        # First need some employees
        # This one will be id 1 and an investigator
        groucho = {
            'name': 'MARX,GROUCHO',
            'grade': 15,
            'step': 1,
            'fte': 80,
            'investigator': 1,
            'notes': 'Really Captain Spaulding'
        }
        result = Employee.add(dao, groucho)
        self.assertEqual(result, 1)
        groucho['id'] = result

        # Try to add a second with same name
        formData = {
            'name': 'MARX,GROUCHO',
            'grade': 12,
            'step': 8,
            'fte': 100,
            'investigator': 0,
            'notes': 'Fake Captain Spaulding'
        }
        expected_err = 'UNIQUE constraint failed: employees.name'
        with self.assertRaises(Exception) as context:
            result = Employee.add(dao, formData)
        self.assertEqual(str(context.exception), expected_err)

        # Add second employee, id will be 2, another investigator
        chico = {
            'name': 'MARX,CHICO',
            'grade': 13,
            'step': 15,
            'fte': 50,
            'investigator': 1,
            'notes': 'Piano Man'
        }
        result = Employee.add(dao, chico)
        self.assertEqual(result, 2)
        chico['id'] = result

        # Add third employee, id will be 3, not investigator
        harpo = {
            'name': 'MARX,HARPO',
            'grade': 12,
            'step': 4,
            'fte': 63,
            'investigator': 0,
            'notes': 'Harpster'
        }
        result = Employee.add(dao, harpo)
        self.assertEqual(result, 3)
        harpo['id'] = result

        # Now have 3 employees
        emps = Employee.get_all(dao)
        self.assertEqual(len(emps), 3)

        # emps is a dictionary
        self.assertDictEqual(emps[1], groucho)

        # Edit employee 1
        formData = {
            'name': 'MARX,GROUCHO',
            'grade': 15,
            'step': 9,
            'fte': 100,
            'investigator': 1,
            'notes': 'Fake Captain Spaulding xxx'
        }
        result = Employee.update(dao, emps[1], formData)
        self.assertEqual(result, 1)     # 1 record affected

        emps[1] = Employee.get_one(dao, 1)
        self.assertEqual(emps[1]['step'], 9)
        self.assertEqual(emps[1]['notes'], 'Fake Captain Spaulding xxx')

        # Add a project, id will be 1
        # PI is Groucho, PM is Harpo
        prjA = {
            'name': 'Test project name',
            'nickname': 'Test project nickname',
            'first_month': '1911',
            'last_month': '2008',
            'PI': groucho['id'],
            'PM': harpo['id'],
            'notes': 'Some notes'
        }
        result = Project.add(dao, prjA)
        self.assertEqual(result, 1)
        prjA['id'] = result

        # Try to add a project with same nickname
        formData = {
            'name': 'Test project name unique',
            'nickname': 'Test project nickname',
            'first_month': '1911',
            'last_month': '2008',
            'PI': groucho['id'],
            'PM': harpo['id'],
            'notes': 'Some notes'
        }
        expected_err = 'UNIQUE constraint failed: projects.nickname'
        with self.assertRaises(Exception) as context:
            result = Project.add(dao, formData)
        self.assertEqual(str(context.exception), expected_err)

        # Try to add a project with same name
        formData = {
            'name': 'Test project name',
            'nickname': 'Test project nickname unique',
            'first_month': '1911',
            'last_month': '2008',
            'PI': groucho['id'],
            'PM': harpo['id'],
            'notes': 'Some notes'
        }
        expected_err = 'UNIQUE constraint failed: projects.name'
        with self.assertRaises(Exception) as context:
            result = Project.add(dao, formData)
        self.assertEqual(str(context.exception), expected_err)

        # Add a second project, id will be 2
        # PI is Chico, PM is Chico
        prjB = {
            'name': 'Another test project name',
            'nickname': 'Another est project nickname',
            'first_month': '1911',
            'last_month': '2008',
            'PI': chico['id'],
            'PM': chico['id'],
            'notes': 'Some notes'
        }
        result = Project.add(dao, prjB)
        self.assertEqual(result, 2)
        prjB['id'] = result

        # Now we have 2 projects
        prjs = Project.get_all(dao)
        self.assertEqual(len(prjs), 2)

        # prjs is a dictionary
        self.assertEqual(prjs[2]['last_month'], '2008')
        self.assertDictEqual(prjs[2], prjB)

        # Edit project 2, change last_month and notes
        prjB = {
            'name': 'Another test project name',
            'nickname': 'Another est project nickname',
            'first_month': '1911',
            'last_month': '2009',
            'PI': 2,
            'PM': 2,
            'notes': 'Some more notes'
        }
        result = Project.update(dao, prjs[2], prjB)
        self.assertEqual(result, 1)     # 1 record affected

        prjs[2] = Project.get_one(dao, 2)
        self.assertEqual(prjs[2]['last_month'], '2009')
        self.assertEqual(prjs[2]['notes'], 'Some more notes')

        # Make assignment for prjA, groucho
        formData = {
            'project_id': prjA['id'],
            'employee_id': groucho['id'],
            'first_month': '1912',
            'last_month': '2004',
            'effort': 50,
            'notes': ''
        }
        result = Assignment.add(dao, formData)
        self.assertEqual(result, 1)

        # Make assignment for prjA, chico
        formData = {
            'project_id': prjA['id'],
            'employee_id': chico['id'],
            'first_month': '1912',
            'last_month': '2004',
            'effort': 50,
            'notes': ''
        }
        result = Assignment.add(dao, formData)
        self.assertEqual(result, 2)

        # Now project 1 has 2 assignments
        asns = Project.getAsns(dao, 1)
        self.assertEqual(len(asns), 2)

        # And project 2 has no assignments
        asns = Project.getAsns(dao, 2)
        self.assertEqual(len(asns), 0)

        # Edit assignment 1

        # Drop project 1, only 1 row affected
        result = Project.delete(dao, [1])
        self.assertEqual(result, 1)

        # Now there's just 1 project
        prjs = Project.get_all(dao)
        self.assertEqual(len(prjs), 1)

        # Project assignments have been deleted
        asns = Project.getAsns(dao, 1)
        self.assertEqual(len(asns), 0)

    def testAddAssignment(self):
        pass

    def testUpdate(self):
        pass

    def testDrop(self):
        pass
