import unittest
from models.validators import *
from models.project import Project
from models.employee import Employee


class ValidationTestSuite(unittest.TestCase):
    def setUp(self):
        self.prjRex = Project.get_all()
        self.empRex = Employee.get_all()

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

        result = validateTimeframe('1406', '1906', self.prjRex[26])
        self.assertEqual(result, 'Timeframe outside project timeframe!')

        result = validateTimeframe('1407', '1907', self.prjRex[26])
        self.assertEqual(result, 'Timeframe outside project timeframe!')

        result = validateTimeframe('1407', '1906', self.prjRex[26])
        self.assertIsNone(result)

    def testEmpName(self):
        result = validateEmpName(None)
        self.assertEqual(result, 'Employee name required!')

        result = validateEmpName('')
        self.assertEqual(result, 'Employee name required!')

        result = validateEmpName('groucho marx', empRex=self.empRex)
        self.assertEqual(result, 'Employee name invalid!')

        result = validateEmpName('marx', empRex=self.empRex)
        self.assertEqual(result, 'Employee name invalid!')

        result = validateEmpName('_marx,groucho', empRex=self.empRex)
        self.assertEqual(result, 'Employee name invalid!')

        result = validateEmpName('marx,groucho:', empRex=self.empRex)
        self.assertEqual(result, 'Employee name invalid!')

        result = validateEmpName('colozzi, john l', empRex=self.empRex)
        self.assertEqual(result, 'Employee name taken!')

        result = validateEmpName('colozzi,john l', empRex=self.empRex)
        self.assertEqual(result, 'Employee name taken!')

        result = validateEmpName('ALDACO-REVILLA,LAURA', empRex=self.empRex)
        self.assertEqual(result, 'Employee name taken!')

        result = validateEmpName('marx, groucho', empRex=self.empRex)
        self.assertIsNone(result)

        result = validateEmpName("o'marx, groucho", empRex=self.empRex)
        self.assertIsNone(result)

        result = validateEmpName("marx, o'groucho", empRex=self.empRex)
        self.assertIsNone(result)

        result = validateEmpName('marx-karl, groucho', empRex=self.empRex)
        self.assertIsNone(result)

        result = validateEmpName('marx, karl-groucho', empRex=self.empRex)
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
