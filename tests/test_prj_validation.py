import unittest
import globals as gbl
import lib.month_lib as ml

errMsg = ''


class TestPrjValidation(unittest.TestCase):

    def validate(self, prj=None):
        import lib.validator_lib as vl

        global errMsg

        prj_id = prj['id'] if prj else 0
        prj_match = vl.ProjectMatch(prj_id, gbl.prjNames)
        errMsg = vl.validatePrjName(self.formData['name'], prj_match)
        if errMsg:
            # vl.showErrMsg(self.txtName, errMsg)
            return False

        prj_match = vl.ProjectMatch(prj_id, gbl.prjNicknames)
        errMsg = vl.validatePrjNickname(self.formData['nickname'], prj_match)
        if errMsg:
            # vl.showErrMsg(self.txtNickname, errMsg)
            return False

        errMsg = vl.validateTimeframe(
            self.formData['first_month'],
            self.formData['last_month']
        )
        if errMsg:
            # vl.showErrMsg(self.txtFirstMonth, errMsg)
            return False

        if prj and 'asns' in prj  and prj['asns']:
            if self.formData['first_month'] < prj['first_month'] or \
                self.formData['last_month'] > prj['last_month']:
                min, max = ml.getTimeframeEdges(prj['asns'])
                if self.formData['first_month'] < min or self.formData['last_month'] > max:
                    errMsg = 'Assignment(s) out of new timeframe!'
                    # vl.showErrMsg(self.txtFirstMonth, errMsg)
                    return False

        return True

    def setUp(self):
        gbl.prjNames = {
            'TESTPROJECTONE': 1,
            'TESTPROJECTTWO': 2,
            'TESTPROJECTTHREE': 3
        }
        gbl.prjNicknames = {
            'TESTPRJ1': 1,
            'TESTPRJ2': 3,
            'TESTPRJ3': 2
        }
        self.formData = {
            'name': '',
            'nickname': '',
            'first_month': '',
            'last_month': ''
        }

    def testValidate(self):
        # Add prj with not name
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Project name required!')

        # Add prj with non-unique name
        self.formData['name'] = 'Test Project Two'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Project name not unique!')

        # Add prj with no nickname
        self.formData['name'] = 'Unique Project Name'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Project nickname required!')

        # Add prj with non-unique nickname
        self.formData['nickname'] = 'Test Prj 3'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Project nickname not unique!')

        # Add prj with no first month
        self.formData['nickname'] = 'Unique prj nickname'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'First month invalid!')

        # Add prj with invalid first month
        self.formData['first_month'] = '1'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'First month invalid!')

        # Add prj with invalid first month
        self.formData['first_month'] = '19'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'First month invalid!')

        # Add prj with invalid first month
        self.formData['first_month'] = '190'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'First month invalid!')

        # Add prj with invalid first month
        self.formData['first_month'] = '1900'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'First month invalid!')

        # Add prj with invalid first month
        self.formData['first_month'] = '1913'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'First month invalid!')

        # Add prj with no last month
        self.formData['first_month'] = '1912'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Last month invalid!')

        # Add prj with invalid last month
        self.formData['last_month'] = '1'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Last month invalid!')

        # Add prj with invalid last month
        self.formData['last_month'] = '19'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Last month invalid!')

        # Add prj with invalid last month
        self.formData['last_month'] = '190'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Last month invalid!')

        # Add prj with invalid last month
        self.formData['last_month'] = '1900'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Last month invalid!')

        # Add prj with invalid last month
        self.formData['last_month'] = '1913'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Last month invalid!')

        # Add prj with invalid last month
        self.formData['last_month'] = '1911'
        result = self.validate()
        self.assertFalse(result)
        self.assertEqual(errMsg, 'First Month must precede Last Month!')

        # Add new prj
        self.formData = {
            'name': 'Test Project Four',
            'nickname': 'Test Prj 4',
            'first_month': '1911',
            'last_month': '2008'
        }
        result = self.validate()
        self.assertTrue(result)
        self.assertIsNone(errMsg)

        prj = {
            'id': 1,
            'name': 'Test Project One',
            'nickname': 'Test Prj 1',
            'first_month': '1809',
            'last_month': '1912'
        }

        # Edit prj name to non-unique value
        self.formData['name'] = 'Test Project Two'
        result = self.validate(prj=prj)
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Project name not unique!')

        # Edit prj nickname to non-unique value
        self.formData['name'] = 'Test Project One'
        self.formData['nickname'] = 'Test Prj 3'
        result = self.validate(prj=prj)
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Project nickname not unique!')

        prj['asns'] = [
            {
                'project_id': 1,
                'first_month': '1809',
                'last_month': '1912'
            },
            {
                'project_id': 1,
                'first_month': '1809',
                'last_month': '1911'
            },
            {
                'project_id': 1,
                'first_month': '1810',
                'last_month': '1912'
            },
        ]

        # Edit prj timeframe out of assignment timeframes
        self.formData = {
            'name': 'Test Project One',
            'nickname': 'Test Prj 1',
            'first_month': '1808',
            'last_month': '1912'
        }
        result = self.validate(prj=prj)
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Assignment(s) out of new timeframe!')

        # Edit prj timeframe out of assignment timeframes
        self.formData = {
            'name': 'Test Project One',
            'nickname': 'Test Prj 1',
            'first_month': '1809',
            'last_month': '2001',
        }
        result = self.validate(prj=prj)
        self.assertFalse(result)
        self.assertEqual(errMsg, 'Assignment(s) out of new timeframe!')

        # Edit prj timeframe but still includes assignment timeframes
        self.formData = {
            'name': 'Test Project One',
            'nickname': 'Test Prj 1',
            'first_month': '1810',
            'last_month': '1912',
        }
        result = self.validate(prj=prj)
        self.assertTrue(result)
        self.assertIsNone(errMsg)

        # Edit prj timeframe but still includes assignment timeframes
        self.formData = {
            'name': 'Test Project One',
            'nickname': 'Test Prj 1',
            'first_month': '1809',
            'last_month': '1911',
        }
        result = self.validate(prj=prj)
        self.assertTrue(result)
        self.assertIsNone(errMsg)

        # Edit field other than name, nickname, timeframe
        self.formData = {
            'name': 'Test Project One',
            'nickname': 'Test Prj 1',
            'first_month': '1809',
            'last_month': '1912',
            'notes': 'bla bla bla'
        }
        result = self.validate(prj=prj)
        self.assertTrue(result)
        self.assertIsNone(errMsg)

