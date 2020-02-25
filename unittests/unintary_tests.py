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

    def test_real_case(self):
        for iteration in range(0, 10000):
            expected = 'sqoop import -fs hdfs://remote-cluster:8020 --hive-drop-import-delims  --fields-terminated-by \; --enclosed-by \'\"\' --escaped-by \\\\ --null-string \'\' --null-non-string \'\' --table sample_table --target-dir hdfs://remote-cluster/user/hive/warehouse/db/sample_table --delete-target-dir  --connect jdbc:oracle:thin:@//your_ip:your_port/your_schema --username user --password pwd --num-mappers 2 --bindir /path/to/bindir/folder'
            sqoop = Sqoop(fs='hdfs://remote-cluster:8020', hive_drop_import_delims=True, fields_terminated_by='\;',
                          enclosed_by='\'"\'', escaped_by='\\\\', null_string='\'\'', null_non_string='\'\'',
                          table='sample_table',
                          target_dir='hdfs://remote-cluster/user/hive/warehouse/db/sample_table',
                          delete_target_dir=True, connect='jdbc:oracle:thin:@//your_ip:your_port/your_schema',
                          username='user', password='pwd', num_mappers=2,
                          bindir='/path/to/bindir/folder')
            self.assertEqual(expected, sqoop.command())
    
    def test_hbase_basic_import(self):
        expected = "sqoop import --table Rutas "\
            "--connect 'jdbc:sqlserver://127.0.0.1:1433;DatabaseName=SQLDB;user=root;password=password' "\
            "--incremental lastmodified --hbase-table Rutas "\
            "--hbase-row-key Id_Ruta -m 1"
        sqoop = Sqoop(
            connect="'jdbc:sqlserver://127.0.0.1:1433;DatabaseName=SQLDB;user=root;password=password'",
            table="Rutas",
            incremental="lastmodified",
            hbase_table="Rutas",
            hbase_row_key="Id_Ruta",
            m=1
            )
        self.assertEqual(expected, sqoop.command())
        
    def test_hbase_lazy_contruction(self):
        expected = "sqoop import --table Rutas "\
            "--connect 'jdbc:sqlserver://127.0.0.1:1433;DatabaseName=SQLDB;user=root;password=password' "\
            "--incremental lastmodified --hbase-table Rutas "\
            "--hbase-row-key Id_Ruta -m 1"
        sqoop = Sqoop()
        sqoop.set_param(param="--connect", value="'jdbc:sqlserver://127.0.0.1:1433;DatabaseName=SQLDB;user=root;password=password'")
        sqoop.set_param(param="--table", value="Rutas")
        sqoop.set_param(param="--incremental", value="lastmodified")
        sqoop.command()
        sqoop.set_param(param="--hbase-table", value="Rutas")
        sqoop.set_param(param="--hbase-row-key", value="Id_Ruta")
        sqoop.set_param(param="-m", value="1")
        self.assertEqual(expected, sqoop.command())

if __name__ == '__main__':
    unittest.main()
