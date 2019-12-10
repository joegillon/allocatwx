import unittest
import globals as gbl

errMsg = ''


class TestEmpValidation(unittest.TestCase):

    def validate(self, emp=None):
        import lib.validator_lib as vl

        global errMsg

        emp_id = emp['id'] if emp else 0
        emp_match = vl.EmployeeMatch(emp_id, gbl.empNames)
        errMsg = vl.validateEmpName(self.formData['name'], emp_match)
        if errMsg:
            # vl.showErrMsg(self.txtName, errMsg)
            return False

        errMsg = vl.validateGrade(self.formData['grade'])
        if errMsg:
            # vl.showErrMsg(self.txtGrade, errMsg)
            return False

        errMsg = vl.validateStep(self.formData['step'])
        if errMsg:
            # vl.showErrMsg(self.txtStep, errMsg)
            return False

        errMsg = vl.validateFte(self.formData['fte'])
        if errMsg:
            # vl.showErrMsg(self.txtFte, errMsg)
            return False

        errMsg = vl.validateInvestigator(
            self.formData['investigator'], self.formData['grade']
        )
        if errMsg:
            # vl.showErrMsg(self.chkInvestigator, errMsg)
            return False

        return True

    def setUp(self):
        gbl.empNames = {
            'MARX,GROUCHO': 1,
            'MARX,CHICO': 2,
            'SNERD,MORTIMER': 3,
            'MCCARTHY-HYPENATED,CHARLIE': 4
        }
        self.formData = {
            'name': '',
            'grade': '',
            'step': '',
            'fte': '',
            'investigator': 0,
            'notes': ''
        }

    def testValidate(self):
        # Add emp with no name
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Employee name required!')

        # Add emp with invalid names
        self.formData['name'] = 'groucho marx'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Employee name invalid!')

        self.formData['name'] = 'marx'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Employee name invalid!')

        self.formData['name'] = '_marx,groucho'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Employee name invalid!')

        self.formData['name'] = 'marx,groucho:'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Employee name invalid!')

        # Let's put a zero in there
        self.formData['name'] = "0'marx,groucho"
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Employee name invalid!')

        # Add emp with non-unique name
        self.formData['name'] = 'marx, groucho'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Employee name not unique!')

        # Add emp with non-unique hyphenated name
        self.formData['name'] = 'mccarthy-hypenated,charlie'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Employee name not unique!')

        # Add emp with valid names
        self.formData['name'] = 'marx, zeppo'
        result = self.validate()
        self.assertTrue(result)
        self.assertIsNone(errMsg)

        self.formData['name'] = "o'marx, zeppo"
        result = self.validate()
        self.assertTrue(result)
        self.assertIsNone(errMsg)

        self.formData['name'] = "marx, O'zeppo"
        result = self.validate()
        self.assertTrue(result)
        self.assertIsNone(errMsg)

        self.formData['name'] = 'marx,karl-zeppo'
        result = self.validate()
        self.assertTrue(result)
        self.assertIsNone(errMsg)

        self.formData['name'] = 'marx-snerd, zeppo'
        result = self.validate()
        self.assertTrue(result)
        self.assertIsNone(errMsg)

        # And if the name is valid and unique the other fields can be blank

        # Now, some invalid grades
        self.formData['grade'] = '-1'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Grade must be number between 0-15!')

        self.formData['grade'] = 'x1'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Grade must be number between 0-15!')

        self.formData['grade'] = '16'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Grade must be number between 0-15!')

        # And valid grades
        self.formData['grade'] = '0'
        result = self.validate()
        self.assertTrue(result)
        self.assertIsNone(errMsg)

        self.formData['grade'] = '15'
        result = self.validate()
        self.assertTrue(result)
        self.assertIsNone(errMsg)

        # Now, some invalid steps
        self.formData['step'] = '-1'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Step must be number between 0-15!')

        self.formData['step'] = 'x1'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Step must be number between 0-15!')

        self.formData['step'] = '16'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Step must be number between 0-15!')

        # And valid steps
        self.formData['step'] = '0'
        result = self.validate()
        self.assertTrue(result)
        self.assertIsNone(errMsg)

        self.formData['step'] = '15'
        result = self.validate()
        self.assertTrue(result)
        self.assertIsNone(errMsg)

        # Now, some invalid ftes
        self.formData['fte'] = '-1'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'FTE must be number between 0-100!')

        self.formData['fte'] = 'x1'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'FTE must be number between 0-100!')

        self.formData['fte'] = '101'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'FTE must be number between 0-100!')

        # And valid steps
        self.formData['fte'] = '0'
        result = self.validate()
        self.assertTrue(result)
        self.assertIsNone(errMsg)

        self.formData['fte'] = '100'
        result = self.validate()
        self.assertTrue(result)
        self.assertIsNone(errMsg)

        # Invalid investigator
        self.formData['grade'] = '12'
        self.formData['investigator'] = 1
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Investigator grade must be >= 13!')