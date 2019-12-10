import unittest
from lib.validator_lib import *


class ValidationTestSuite(unittest.TestCase):
    def setUp(self):
        self.prjNames = {
            'TESTNAME1': 41,
            'TESTNAME2': 23,
            'TESTNAME3': 18
        }
        self.prjNicknames = {
            'TESTNICKNAME1': 41,
            'TESTNICKNAME2': 23,
            'TESTNICKNAME3': 18
        }
        self.empNames = {
            'MARX,GROUCHO': 1,
            'MARX,CHICO': 2,
            'MARX,HARPO': 3,
            'NAME-HYPHENATED,BOZO': 99
        }

    def testName(self):
        # Set current project to ID 18 (Test Name 3)
        prj_match = ProjectMatch(18, self.prjNames)

        # Project name cannot be None
        result = validatePrjName(None, prj_match)
        self.assertEqual(result, 'Project name required!')

        # Project name cannot be ''
        result = validatePrjName('', prj_match)
        self.assertEqual(result, 'Project name required!')

        # Project name must be unique
        result = validatePrjName('test  name 2', prj_match)
        self.assertEqual(result, 'Project name taken!')

        # Now we have a match but it's the current project
        result = validatePrjName('test  name 3', prj_match)
        self.assertIsNone(result)

        result = validatePrjName('Unused project name', prj_match)
        self.assertIsNone(result)

    def testNickname(self):
        # Set current project to ID 18 (Test Name 3)
        prj_match = ProjectMatch(18, self.prjNicknames)

        result = validatePrjNickname(None, prj_match)
        self.assertEqual(result, 'Project nickname required!')

        result = validatePrjNickname('', prj_match)
        self.assertEqual(result, 'Project nickname required!')

        result = validatePrjNickname('test  nickname 1', prj_match)
        self.assertEqual(result, 'Project nickname taken!')

        result = validatePrjNickname('test  nickname 3', prj_match)
        self.assertIsNone(result)

        result = validatePrjNickname('Unused project nickname', prj_match)
        self.assertIsNone(result)

    def testTimeframe(self):
        result = validateTimeframe('', '')
        self.assertEqual(result, 'First month invalid!')

        result = validateTimeframe('00', '')
        self.assertEqual(result, 'First month invalid!')

        result = validateTimeframe('01', '')
        self.assertEqual(result, 'First month invalid!')

        result = validateTimeframe('010', '')
        self.assertEqual(result, 'First month invalid!')

        result = validateTimeframe('0000', '')
        self.assertEqual(result, 'First month invalid!')

        result = validateTimeframe('0013', '')
        self.assertEqual(result, 'First month invalid!')

        result = validateTimeframe('0001', '')
        self.assertEqual(result, 'Last month invalid!')

        result = validateTimeframe('0001', '00')
        self.assertEqual(result, 'Last month invalid!')

        result = validateTimeframe('0001', '010')
        self.assertEqual(result, 'Last month invalid!')

        result = validateTimeframe('0001', '0000')
        self.assertEqual(result, 'Last month invalid!')

        result = validateTimeframe('0001', '0013')
        self.assertEqual(result, 'Last month invalid!')

        result = validateTimeframe('0001', '00131')
        self.assertEqual(result, 'Last month invalid!')

        result = validateTimeframe('1902', '1901')
        self.assertEqual(result, 'First Month must precede Last Month!')

        result = validateTimeframe('1901', '1812')
        self.assertEqual(result, 'First Month must precede Last Month!')

        result = validateTimeframe('1912', '2001')
        self.assertIsNone(result)

        prj = {
            'name': 'Any name',
            'nickname': 'Any nickname',
            'first_month': '1407',
            'last_month': '1906'
        }
        result = validateAsnTimeframe('1406', '1906', prj)
        self.assertEqual(result, 'Timeframe outside project timeframe!')

        prj['first_month'] = '1407'
        result = validateAsnTimeframe('1407', '1907', prj)
        self.assertEqual(result, 'Timeframe outside project timeframe!')

        prj['last_month'] = '1906'
        result = validateAsnTimeframe('1407', '1906', prj)
        self.assertIsNone(result)

    def testEmpName(self):
        emp_match = EmployeeMatch(1, self.empNames)

        result = validateEmpName(None)
        self.assertEqual(result, 'Employee name required!')

        result = validateEmpName('')
        self.assertEqual(result, 'Employee name required!')

        result = validateEmpName('groucho marx', emp_match)
        self.assertEqual(result, 'Employee name invalid!')

        result = validateEmpName('marx', emp_match)
        self.assertEqual(result, 'Employee name invalid!')

        result = validateEmpName('_marx,groucho', emp_match)
        self.assertEqual(result, 'Employee name invalid!')

        result = validateEmpName('marx,groucho:', emp_match)
        self.assertEqual(result, 'Employee name invalid!')

        result = validateEmpName('marx,  groucho', emp_match)
        self.assertIsNone(result)

        result = validateEmpName('marx,harpo', emp_match)
        self.assertEqual(result, 'Employee name taken!')

        result = validateEmpName('name-hyphenated,bozo', emp_match)
        self.assertEqual(result, 'Employee name taken!')

        result = validateEmpName('marx, zeppo', emp_match)
        self.assertIsNone(result)

        result = validateEmpName("o'marx, groucho", emp_match)
        self.assertIsNone(result)

        result = validateEmpName("marx, o'groucho", emp_match)
        self.assertIsNone(result)

        result = validateEmpName('marx-karl, groucho', emp_match)
        self.assertIsNone(result)

        result = validateEmpName('marx, karl-groucho', emp_match)
        self.assertIsNone(result)

    def testGrade(self):
        result = validateGrade(None)
        self.assertIsNone(result)

        result = validateGrade("")
        self.assertIsNone(result)

        result = validateGrade('x2')
        self.assertEqual(result, 'Grade must be number between 0-15!')

        result = validateGrade('-1')
        self.assertEqual(result, 'Grade must be number between 0-15!')

        result = validateGrade('16')
        self.assertEqual(result, 'Grade must be number between 0-15!')

        result = validateGrade('0')
        self.assertIsNone(result)

        result = validateGrade('15')
        self.assertIsNone(result)

        result = validateGrade('2')
        self.assertIsNone(result)

    def testStep(self):
        result = validateStep(None)
        self.assertIsNone(result)

        result = validateStep("")
        self.assertIsNone(result)

        result = validateStep('x2')
        self.assertEqual(result, 'Step must be number between 0-15!')

        result = validateStep('-1')
        self.assertEqual(result, 'Step must be number between 0-15!')

        result = validateStep('16')
        self.assertEqual(result, 'Step must be number between 0-15!')

        result = validateStep('0')
        self.assertIsNone(result)

        result = validateStep('15')
        self.assertIsNone(result)

        result = validateStep('2')
        self.assertIsNone(result)

    def testFte(self):
        result = validateFte(None)
        self.assertIsNone(result)

        result = validateFte("")
        self.assertIsNone(result)

        result = validateFte('x2')
        self.assertEqual(result, 'FTE must be number between 0-100!')

        result = validateFte('-1')
        self.assertEqual(result, 'FTE must be number between 0-100!')

        result = validateFte('101')
        self.assertEqual(result, 'FTE must be number between 0-100!')

        result = validateFte('0')
        self.assertIsNone(result)

        result = validateFte('100')
        self.assertIsNone(result)

        result = validateFte('22')
        self.assertIsNone(result)

    def testEffort(self):
        result = validateEffort(None)
        self.assertEqual(result, 'Percent effort required!')

        result = validateEffort("")
        self.assertEqual(result, 'Percent effort required!')

        result = validateEffort('x2')
        self.assertEqual(result, 'Percent effort must be number between 0-100!')

        result = validateEffort('-1')
        self.assertEqual(result, 'Percent effort must be number between 0-100!')

        result = validateEffort('101')
        self.assertEqual(result, 'Percent effort must be number between 0-100!')

        result = validateEffort('0')
        self.assertIsNone(result)

        result = validateEffort('100')
        self.assertIsNone(result)

        result = validateEffort('22')
        self.assertIsNone(result)
