import unittest
from dal.dao import Dao
import dal.asn_dal as asn_dal
import dal.emp_dal as emp_dal
import dal.prj_dal as prj_dal
from tests.setup_db import getDB

mockDB = getDB()


class TestProject(unittest.TestCase):

    def testAdd(self):
        dao = Dao(stateful=True, db=mockDB)

        # First need some employees
        # This one will be id 1 and an investigator
        groucho = {
            'name': 'MARX,GROUCHO',
            'grade': '',
            'step': '',
            'fte': '',
            'investigator': 1,
            'notes': ''
        }
        result = emp_dal.add(dao, groucho)
        self.assertEqual(result, 1)
        groucho['id'] = result

        # Try to add a second with same name
        chico = {
            'name': 'MARX,GROUCHO',
            'grade': 13,
            'step': 15,
            'fte': 50,
            'investigator': 1,
            'notes': 'Piano Man'
        }
        expected_err = 'Employee name is not unique!'
        with self.assertRaises(Exception) as context:
            result = emp_dal.add(dao, chico)
        self.assertEqual(str(context.exception), expected_err)

        # Add second employee, id will be 2, another investigator
        chico['name'] = 'MARX,CHICO'
        result = emp_dal.add(dao, chico)
        self.assertEqual(result, 2)
        chico['id'] = result

        formData = {
            'name': 'MARX,GROUCHO',
            'grade': 15,
            'step': 4,
            'fte': 80,
            'investigator': 1,
            'notes': 'AKA Captain Spaulding'
        }
        result = emp_dal.update(dao, groucho, formData)
        self.assertEqual(result, 1)
        groucho = emp_dal.get_one(dao, groucho['id'])
        self.assertEqual(groucho['grade'], 15)
        self.assertEqual(groucho['step'], 4)
        self.assertEqual(groucho['fte'], 80)
        self.assertEqual(groucho['notes'], 'AKA Captain Spaulding')

        # Add third employee, id will be 3, not investigator
        harpo = {
            'name': 'MARX,HARPO',
            'grade': 12,
            'step': 4,
            'fte': 63,
            'investigator': 0,
            'notes': 'Harpster'
        }
        result = emp_dal.add(dao, harpo)
        self.assertEqual(result, 3)
        harpo['id'] = result

        formData = {
            'name': 'MARX,CHICO',
            'grade': 12,
            'step': 4,
            'fte': 63,
            'investigator': 0,
            'notes': 'Harpster'
        }
        expected_err = 'Employee name is not unique!'
        with self.assertRaises(Exception) as context:
            result = emp_dal.update(dao, harpo, formData)
        self.assertEqual(str(context.exception), expected_err)

        # Now have 3 employees
        emps = emp_dal.get_all(dao)
        self.assertEqual(len(emps), 3)

        # emps is a dictionary
        self.assertDictEqual(emps[1], groucho)
        self.assertDictEqual(emps[2], chico)
        self.assertDictEqual(emps[3], harpo)

        # Edit employee 1
        formData = {
            'name': 'MARX,GROUCHO',
            'grade': 15,
            'step': 9,
            'fte': 100,
            'investigator': 1,
            'notes': 'Three chairs for Captain Spaulding!'
        }
        result = emp_dal.update(dao, emps[1], formData)
        self.assertEqual(result, 1)     # 1 record affected

        emps[1] = emp_dal.get_one(dao, 1)
        self.assertEqual(emps[1]['step'], 9)
        self.assertEqual(emps[1]['notes'], 'Three chairs for Captain Spaulding!')

        # Add a project, id will be 1
        prjA = {
            'name': 'Project A',
            'nickname': 'Prj A',
            'first_month': '1911',
            'last_month': '2008',
            'PI': None,
            'PM': None,
            'notes': ''
        }
        result = prj_dal.add(dao, prjA)
        self.assertEqual(result, 1)
        prjA['id'] = result

        prjA['PI'] = groucho['id']
        prjA['PM'] = harpo['id']
        result = prj_dal.update(dao, prjA, prjA)
        self.assertEqual(result, 1)

        # Try to add a project with same nickname
        formData = {
            'name': 'Test project name unique',
            'nickname': 'Prj A',
            'first_month': '1911',
            'last_month': '2008',
            'PI': groucho['id'],
            'PM': harpo['id'],
            'notes': 'Some notes'
        }
        expected_err = 'Project nickname is not unique!'
        with self.assertRaises(Exception) as context:
            result = prj_dal.add(dao, formData)
        self.assertEqual(str(context.exception), expected_err)

        # Try to add a project with same name
        formData = {
            'name': 'Project A',
            'nickname': 'Test project nickname unique',
            'first_month': '1911',
            'last_month': '2008',
            'PI': groucho['id'],
            'PM': harpo['id'],
            'notes': 'Some notes'
        }
        expected_err = 'Project name is not unique!'
        with self.assertRaises(Exception) as context:
            result = prj_dal.add(dao, formData)
        self.assertEqual(str(context.exception), expected_err)

        # Add a second project, id will be 2
        # PI is Chico, PM is Chico
        prjB = {
            'name': 'Project B',
            'nickname': 'Prj B',
            'first_month': '1911',
            'last_month': '2008',
            'PI': chico['id'],
            'PM': chico['id'],
            'notes': 'Some notes'
        }
        result = prj_dal.add(dao, prjB)
        self.assertEqual(result, 2)
        prjB['id'] = result

        # Now we have 2 projects
        prjs = prj_dal.get_all(dao)
        self.assertEqual(len(prjs), 2)

        # prjs is a dictionary
        self.assertEqual(prjs[2]['last_month'], '2008')
        self.assertDictEqual(prjs[2], prjB)

        # Try to change prjB name to prjA name
        formData = {
            'name': 'Project A',
            'nickname': 'Prj B',
            'first_month': '1911',
            'last_month': '2008',
            'PI': chico['id'],
            'PM': chico['id'],
            'notes': 'Some notes'
        }
        expected_err = 'Project name is not unique!'
        with self.assertRaises(Exception) as context:
            result = prj_dal.update(dao, prjB, formData)
        self.assertEqual(str(context.exception), expected_err)

        # Try to change prjB nickname to prjA name
        formData = {
            'name': 'Project B',
            'nickname': 'Prj A',
            'first_month': '1911',
            'last_month': '2008',
            'PI': chico['id'],
            'PM': chico['id'],
            'notes': 'Some notes'
        }
        expected_err = 'Project nickname is not unique!'
        with self.assertRaises(Exception) as context:
            result = prj_dal.update(dao, prjB, formData)
        self.assertEqual(str(context.exception), expected_err)

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
        result = prj_dal.update(dao, prjs[2], prjB)
        self.assertEqual(result, 1)     # 1 record affected

        prjs[2] = prj_dal.get_one(dao, 2)
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
        result = asn_dal.add(dao, formData)
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
        result = asn_dal.add(dao, formData)
        self.assertEqual(result, 2)

        # Now project 1 has 2 assignments
        asns = prj_dal.getAsns(dao, 1)
        self.assertEqual(len(asns), 2)

        # And project 2 has no assignments
        asns = prj_dal.getAsns(dao, 2)
        self.assertEqual(len(asns), 0)

        # Edit assignment 1

        # Drop project 1, only 1 row affected
        result = prj_dal.delete(dao, [1])
        self.assertEqual(result, 1)

        # Now there's just 1 project
        prjs = prj_dal.get_all(dao)
        self.assertEqual(len(prjs), 1)

        # Project assignments have been deleted
        asns = prj_dal.getAsns(dao, 1)
        self.assertEqual(len(asns), 0)
