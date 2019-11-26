import unittest
from models.validators import *
from models.project import Project


class PrjValidationTest(unittest.TestCase):
    def setUp(self):
        self.prjRex = Project.get_all()

    def testName(self):
        result = validatePrjName(None, self.prjRex)
        self.assertEqual(result, 'Project name required!')

        result = validatePrjName('', self.prjRex)
        self.assertEqual(result, 'Project name required!')

        value = 'CDA 17-169 Assessing Treatment Delay and Resource Use to Improve Value of Pre-Surgical Care'
        result = validatePrjName(value, self.prjRex)
        self.assertEqual(result, 'Project name taken!')

        value = 'Unused project name'
        result = validatePrjName(value, self.prjRex)
        self.assertIsNone(result)

    def testNickname(self):
        value = None
        result = validatePrjNickname(value, self.prjRex)
        self.assertEqual(result, 'Project nickname required!')

        value = ''
        result = validatePrjNickname(value, self.prjRex)
        self.assertEqual(result, 'Project nickname required!')

        value = 'CDA 17-169 (Sears)'
        result = validatePrjNickname(value, self.prjRex)
        self.assertEqual(result, 'Project nickname taken!')

        value = 'Unused project nickname'
        result = validatePrjNickname(value, self.prjRex)
        self.assertIsNone(result)

    def testTimeframe(self):
        result = validateTimeframe('', '')
        self.assertEqual(result, 'First month invalid!')

        result = validateTimeframe('00/', '')
        self.assertEqual(result, 'First month invalid!')

        result = validateTimeframe('01/', '')
        self.assertEqual(result, 'First month invalid!')

        result = validateTimeframe('01/0', '')
        self.assertEqual(result, 'First month invalid!')

        result = validateTimeframe('00/00', '')
        self.assertEqual(result, 'First month invalid!')

        result = validateTimeframe('13/00', '')
        self.assertEqual(result, 'First month invalid!')

        result = validateTimeframe('01/00', '')
        self.assertEqual(result, 'Last month invalid!')

        result = validateTimeframe('01/00', '00/')
        self.assertEqual(result, 'Last month invalid!')

        result = validateTimeframe('01/00', '01/0')
        self.assertEqual(result, 'Last month invalid!')

        result = validateTimeframe('01/00', '00/00')
        self.assertEqual(result, 'Last month invalid!')

        result = validateTimeframe('01/00', '13/00')
        self.assertEqual(result, 'Last month invalid!')

        result = validateTimeframe('02/19', '01/19')
        self.assertEqual(result, 'First Month must precede Last Month!')

        result = validateTimeframe('01/19', '12/18')
        self.assertEqual(result, 'First Month must precede Last Month!')

        result = validateTimeframe('12/19', '01/20')
        self.assertIsNone(result)

        result = validateTimeframe('06/14', '06/19', self.prjRex[26])
        self.assertEqual(result, 'Timeframe outside project timeframe!')

        result = validateTimeframe('07/14', '07/19', self.prjRex[26])
        self.assertEqual(result, 'Timeframe outside project timeframe!')

        result = validateTimeframe('07/14', '06/19', self.prjRex[26])
        self.assertIsNone(result)

    def testEmpName(self):
        result = validateEmpName(None)
        self.assertEqual(result, 'Employee name required!')

        result = validateEmpName('')
        self.assertEqual(result, 'Employee name required!')

        result = validateEmpName('groucho marx', chk=True)
        self.assertEqual(result, 'Employee name invalid!')

        result = validateEmpName('marx', chk=True)
        self.assertEqual(result, 'Employee name invalid!')

        result = validateEmpName('_marx,groucho', chk=True)
        self.assertEqual(result, 'Employee name invalid!')

        result = validateEmpName('marx,groucho:', chk=True)
        self.assertEqual(result, 'Employee name invalid!')

        result = validateEmpName('marx, groucho', chk=True)
        self.assertIsNone(result)

        result = validateEmpName("o'marx, groucho", chk=True)
        self.assertIsNone(result)

        result = validateEmpName("marx, o'groucho", chk=True)
        self.assertIsNone(result)

        result = validateEmpName('marx-karl, groucho', chk=True)
        self.assertIsNone(result)

        result = validateEmpName('marx, karl-groucho', chk=True)
        self.assertIsNone(result)

    def testEffort(self):
        result = validateEffort(None)
        self.assertEqual(result, 'Percent effort required!')

        result = validateEffort("")
        self.assertEqual(result, 'Percent effort required!')

        result = validateEffort('x2')
        self.assertEqual(result, 'Percent effort must be numeric!')

        result = validateEffort('-1')
        self.assertEqual(result, 'Percent effort must be between 0-100!')

        result = validateEffort('101')
        self.assertEqual(result, 'Percent effort must be between 0-100!')

        result = validateEffort('0')
        self.assertIsNone(result)

        result = validateEffort('100')
        self.assertIsNone(result)

        result = validateEffort('22')
        self.assertIsNone(result)
