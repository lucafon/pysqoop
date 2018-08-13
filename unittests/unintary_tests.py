import unittest
from pysqoop.pysqoop.SqoopImport import Sqoop


class TestStringMethods(unittest.TestCase):

    def test_empty_sqoop(self):
        try:
            Sqoop()
        except Exception as e:
            self.assertEqual(str(e), 'all parameters are empty')

    def test_properties_not_empty(self):
        try:
            Sqoop(fields_terminated_by='\"')
        except Exception as e:
            self.assertEqual(str(e), Sqoop._EMPTY_TABLE_AND_QUERY_PARAMETERS_EXCEPTION)

    def test_parameters_order(self):
        for iteration in range(0, 10000):
            sqoop = Sqoop(null_string='\'\'', fields_terminated_by='\"', table='prova')
            self.assertEqual(sqoop.command(), 'sqoop import --fields-terminated-by \" --null-string \'\' --table prova')

if __name__ == '__main__':
    unittest.main()
