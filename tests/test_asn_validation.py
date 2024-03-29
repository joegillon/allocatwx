import unittest
import globals as gbl

errMsg = ''


class DummyOwner(object):
    def __init__(self, name):
        self.name = name


class TestAsnValidation(unittest.TestCase):

    def validate(self):
        import lib.validator_lib as vl

        global errMsg

        if self.cboOwner:
            if not self.formData['owner']:
                errMsg = '%s is required!' % self.cboOwner.name
                # vl.showErrMsg(self.cboOwner, errMsg)
                return False

        errMsg = vl.validateTimeframe(
            self.formData['first_month'],
            self.formData['last_month'])
        if errMsg:
            # vl.showErrMsg(self.txtFirstMonth, errMsg)
            return False

        errMsg = vl.validateEffort(self.formData['effort'])
        if errMsg:
            # vl.showErrMsg(self.txtEffort, errMsg)
            return False

        errMsg = vl.validateAsnTimeframe(
            self.formData['first_month'],
            self.formData['last_month'],
            gbl.prjRex[self.formData['project_id']]
        )
        if errMsg:
            # vl.showErrMsg(self.txtFirstMonth, errMsg)
            return False

        return True

    def setUp(self):
        self.cboOwner = None
        self.formData = {
            'owner': '',
            'first_month': '',
            'last_month': '',
            'effort': '',
            'project_id': 2
        }
        gbl.prjRex = {
            1: {'id': 1},
            2: {'id': 2, 'first_month': '1910', 'last_month': '2009'},
            3: {'id': 3}
        }

    def testValidate(self):
        # No first month
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'First month invalid!')

        # Invalid first month
        self.formData['first_month'] = '1'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'First month invalid!')

        # Invalid first month
        self.formData['first_month'] = '19'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'First month invalid!')

        # Invalid first month
        self.formData['first_month'] = '190'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'First month invalid!')

        # Invalid first month
        self.formData['first_month'] = '1900'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'First month invalid!')

        # Invalid first month
        self.formData['first_month'] = '1913'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'First month invalid!')

        # No last month
        self.formData['first_month'] = '1912'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Last month invalid!')

        # Invalid last month
        self.formData['last_month'] = '1'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Last month invalid!')

        # Invalid last month
        self.formData['last_month'] = '19'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Last month invalid!')

        # Invalid last month
        self.formData['last_month'] = '190'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Last month invalid!')

        # Invalid last month
        self.formData['last_month'] = '1900'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Last month invalid!')

        # Invalid last month
        self.formData['last_month'] = '1913'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Last month invalid!')

        # Invalid last month
        self.formData['last_month'] = '1911'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'First Month must precede Last Month!')

        # No effort
        self.formData['last_month'] = '2001'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Percent effort required!')

        # Invalid effort
        self.formData['effort'] = 'x2'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Percent effort must be number between 0-100!')

        # Invalid effort
        self.formData['effort'] = '-1'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Percent effort must be number between 0-100!')

        # Invalid effort
        self.formData['effort'] = '101'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Percent effort must be number between 0-100!')

        # Valid effort
        self.formData['effort'] = '0'
        result = self.validate()
        self.assertTrue(result)
        self.assertIsNone(errMsg)

        # Valid effort
        self.formData['effort'] = '100'
        result = self.validate()
        self.assertTrue(result)
        self.assertIsNone(errMsg)

        # Add the asn (requires an owner)
        self.cboOwner = DummyOwner('Project')
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Project is required!')

        # Add the asn (requires an owner)
        self.cboOwner = DummyOwner('Employee')
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Employee is required!')

        # Add the asn (requires an owner)
        self.formData['owner'] = 'Some project'
        self.cboOwner = DummyOwner('Project')
        result = self.validate()
        self.assertTrue(result)
        self.assertIsNone(errMsg)

        # Asn outside prj timeframe
        self.formData['project_id'] = 2
        self.formData['first_month'] = '1909'
        self.formData['last_month'] = '2009'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Timeframe outside project timeframe!')

        # Asn outside prj timeframe
        self.formData['project_id'] = 2
        self.formData['first_month'] = '1910'
        self.formData['last_month'] = '2010'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Timeframe outside project timeframe!')

        # Asn in prj timeframe
        self.formData['project_id'] = 2
        self.formData['first_month'] = '1910'
        self.formData['last_month'] = '2009'
        result = self.validate()
        self.assertTrue(result)
        self.assertIsNone(errMsg)
