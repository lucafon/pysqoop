import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pysqoop'))
from pysqoop.SqoopImport import Sqoop


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
            expected = 'sqoop import -fs hdfs://remote-cluster:8020 --hive-drop-import-delims  --fields-terminated-by \\; --enclosed-by \'"\' --escaped-by \\\\ --null-string \'\' --null-non-string \'\' --table sample_table --target-dir hdfs://remote-cluster/user/hive/warehouse/db/sample_table --delete-target-dir  --connect jdbc:oracle:thin:@//your_ip:your_port/your_schema --username user --password pwd --num-mappers 2 --bindir /path/to/bindir/folder'
            sqoop = Sqoop(fs='hdfs://remote-cluster:8020', hive_drop_import_delims=True, fields_terminated_by='\\;',
                          enclosed_by='\'"\'', escaped_by='\\\\', null_string='\'\'', null_non_string='\'\'',
                          table='sample_table',
                          target_dir='hdfs://remote-cluster/user/hive/warehouse/db/sample_table',
                          delete_target_dir=True, connect='jdbc:oracle:thin:@//your_ip:your_port/your_schema',
                          username='user', password='pwd', num_mappers=2,
                          bindir='/path/to/bindir/folder')
            self.assertEqual(expected, sqoop.command())

    def test_hbase_basic_import(self):
        expected = "sqoop import --table Rutas " \
                   "--connect 'jdbc:sqlserver://127.0.0.1:1433;DatabaseName=SQLDB;user=root;password=password' " \
                   "--incremental lastmodified --hbase-table Rutas --column-family Id_Ruta " \
                   "--hbase-row-key Id_Ruta -m 1"
        sqoop = Sqoop(
            connect="'jdbc:sqlserver://127.0.0.1:1433;DatabaseName=SQLDB;user=root;password=password'",
            table="Rutas",
            incremental="lastmodified",
            hbase_table="Rutas",
            hbase_row_key="Id_Ruta",
            column_family="Id_Ruta",
            m=1
        )
        self.assertEqual(expected, sqoop.command())

    def test_hbase_lazy_contruction(self):
        expected = "sqoop import --table Rutas " \
                   "--connect 'jdbc:sqlserver://127.0.0.1:1433;DatabaseName=SQLDB;user=root;password=password' " \
                   "--incremental lastmodified --hbase-table Rutas --column-family Id_Ruta " \
                   "--hbase-row-key Id_Ruta -m 1"
        sqoop = Sqoop()
        sqoop.set_param(param="--connect",
                        value="'jdbc:sqlserver://127.0.0.1:1433;DatabaseName=SQLDB;user=root;password=password'")
        sqoop.set_param(param="--table", value="Rutas")
        sqoop.set_param(param="--incremental", value="lastmodified")
        # sqoop.unset_param(param="--connect")
        sqoop.command()
        sqoop.set_param(param="--hbase-table", value="Rutas")
        sqoop.set_param(param="--column-family", value="Id_Ruta")
        sqoop.set_param(param="--hbase-row-key", value="Id_Ruta")
        sqoop.set_param(param="-m", value="1")
        self.assertEqual(expected, sqoop.command())

    def test_java_opts_functionality(self):
        """Test java_opts parameter handling - fixes issue #13"""

        # Test without java_opts
        sqoop_no_opts = Sqoop(table='test_table')
        cmd_no_opts = sqoop_no_opts.command()
        self.assertEqual(cmd_no_opts, 'sqoop import --table test_table')
        self.assertNotIn('None', cmd_no_opts)

        # Test with java_opts
        sqoop_with_opts = Sqoop(table='test_table', java_opts='-Xmx1024m')
        cmd_with_opts = sqoop_with_opts.command()
        self.assertEqual(cmd_with_opts, 'sqoop import -Xmx1024m --table test_table')

        # Test java_opts is placed at the beginning
        self.assertTrue(cmd_with_opts.startswith('sqoop import -Xmx1024m'))

        # Test with empty java_opts
        sqoop_empty_opts = Sqoop(table='test_table', java_opts='')
        cmd_empty_opts = sqoop_empty_opts.command()
        self.assertEqual(cmd_empty_opts, 'sqoop import --table test_table')

        # Test with None java_opts explicitly
        sqoop_none_opts = Sqoop(table='test_table', java_opts=None)
        cmd_none_opts = sqoop_none_opts.command()
        self.assertEqual(cmd_none_opts, 'sqoop import --table test_table')

        # Test export command with java_opts
        sqoop_export = Sqoop(table='test_table', java_opts='-Xmx512m', export_dir='/path/to/export')
        export_cmd = sqoop_export.export_command()
        self.assertEqual(export_cmd, 'sqoop export -Xmx512m --table test_table --export-dir /path/to/export')

        # Test export command without java_opts
        sqoop_export_no_opts = Sqoop(table='test_table', export_dir='/path/to/export')
        export_cmd_no_opts = sqoop_export_no_opts.export_command()
        self.assertEqual(export_cmd_no_opts, 'sqoop export --table test_table --export-dir /path/to/export')

        # Test complex command with java_opts and multiple parameters
        sqoop_complex = Sqoop(
            table='complex_table',
            java_opts='-Xmx2048m -Djava.security.egd=file:/dev/urandom',
            username='user',
            password='pass',
            num_mappers=4
        )
        complex_cmd = sqoop_complex.command()
        expected_complex = 'sqoop import -Xmx2048m -Djava.security.egd=file:/dev/urandom --table complex_table --username user --password pass --num-mappers 4'
        self.assertEqual(complex_cmd, expected_complex)


if __name__ == '__main__':
    unittest.main()
