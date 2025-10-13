import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pysqoop'))
from pysqoop.SqoopImport import Sqoop
from pysqoop.SqoopJob import SqoopJob
from pysqoop.MapredJob import MapredJob


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

    def test_export_command_functionality(self):
        """Test export command building and functionality"""

        # Basic export command
        sqoop = Sqoop(table='export_table', export_dir='/path/to/export/data')
        export_cmd = sqoop.export_command()
        expected = 'sqoop export --table export_table --export-dir /path/to/export/data'
        self.assertEqual(export_cmd, expected)

        # Export with additional parameters
        sqoop_complex = Sqoop(
            table='complex_export',
            export_dir='/hdfs/export/path',
            connect='jdbc:mysql://localhost:3306/testdb',
            username='testuser',
            password='testpass',
            num_mappers=4
        )
        complex_export_cmd = sqoop_complex.export_command()
        expected_complex = 'sqoop export --table complex_export --connect jdbc:mysql://localhost:3306/testdb --username testuser --password testpass --num-mappers 4 --export-dir /hdfs/export/path'
        self.assertEqual(complex_export_cmd, expected_complex)

    def test_properties_method(self):
        """Test the properties() method returns correct dictionary"""

        sqoop = Sqoop(table='test_table', username='user', password='pass')
        props = sqoop.properties()

        # Check it returns a dictionary
        self.assertIsInstance(props, dict)

        # Check some key properties are present
        self.assertIn('--table', props)
        self.assertIn('--username', props)
        self.assertIn('--password', props)

        # Check values are correct
        self.assertEqual(props['--table'], 'test_table')
        self.assertEqual(props['--username'], 'user')
        self.assertEqual(props['--password'], 'pass')

        # Check None properties are also included
        self.assertIn('--connect', props)
        self.assertIsNone(props['--connect'])

    def test_unset_param_method(self):
        """Test the unset_param() method functionality"""

        sqoop = Sqoop(table='test_table', username='user', password='pass')

        # Test unsetting an existing parameter
        result = sqoop.unset_param('--username')
        self.assertTrue(result)
        self.assertIsNone(sqoop.properties()['--username'])

        # Test unsetting a non-existent parameter
        result = sqoop.unset_param('--nonexistent')
        self.assertFalse(result)

        # Test that command reflects the unset parameter
        cmd = sqoop.command()
        self.assertNotIn('--username', cmd)
        self.assertIn('--table test_table', cmd)
        self.assertIn('--password pass', cmd)

    def test_perform_import_without_sqoop_installed(self):
        """Test perform_import() behavior when sqoop is not installed"""

        sqoop = Sqoop(help=True)
        result = sqoop.perform_import()

        # Should return CompletedProcess or integer (90 for error)
        self.assertTrue(
            hasattr(result, 'returncode') or isinstance(result, int),
            "perform_import should return CompletedProcess or error code"
        )

        # If CompletedProcess, check it has expected attributes
        if hasattr(result, 'returncode'):
            self.assertTrue(hasattr(result, 'stdout'))
            self.assertTrue(hasattr(result, 'stderr'))

    def test_perform_export_without_sqoop_installed(self):
        """Test perform_export() behavior when sqoop is not installed"""

        sqoop = Sqoop(table='test_table', export_dir='/test/path')
        result = sqoop.perform_export()

        # Should return integer (exit code)
        self.assertIsInstance(result, int)

    def test_validation_errors(self):
        """Test _perform_checks() validation errors"""

        # Test empty table and query error
        with self.assertRaises(Exception) as context:
            sqoop = Sqoop(username='user')  # No table or query
            sqoop.command()

        self.assertIn('--table or --query is required', str(context.exception))

        # Test incremental validation error
        with self.assertRaises(Exception) as context:
            sqoop = Sqoop(table='test', incremental='invalid_mode')
            sqoop.command()

        self.assertIn("incremental needs either 'append' or 'lastmodified'", str(context.exception))

    def test_hbase_validation_errors(self):
        """Test HBase parameter validation"""

        # Test missing hbase-row-key
        with self.assertRaises(Exception) as context:
            sqoop = Sqoop(table='test', hbase_table='test_hbase')
            sqoop.command()

        self.assertIn('--hbase-table needs the --hbase-row-key and --column-family', str(context.exception))

        # Test missing hbase-table
        with self.assertRaises(Exception) as context:
            sqoop = Sqoop(table='test', hbase_row_key='row_key')
            sqoop.command()

        self.assertIn('--hbase-row-key needs the --hbase-table and --column-family', str(context.exception))

        # Test missing hbase-table and row-key for column-family
        with self.assertRaises(Exception) as context:
            sqoop = Sqoop(table='test', column_family='cf1')
            sqoop.command()

        self.assertIn('--column-family needs the --hbase-table and --hbase-row-key', str(context.exception))

    def test_oracle_partition_functionality(self):
        """Test Oracle partition parameter handling"""

        sqoop = Sqoop(table='test_table', oracle_partition='PARTITION_01')
        cmd = sqoop.command()

        # Should include Oracle partition parameter
        self.assertIn('-Doraoop.import.partitions=PARTITION_01', cmd)
        self.assertIn('--table test_table', cmd)

    def test_boolean_parameters(self):
        """Test boolean parameter handling"""

        sqoop = Sqoop(
            table='test_table',
            hive_import=True,
            hive_overwrite=True,
            as_textfile=True,
            delete_target_dir=True,
            direct=True
        )

        cmd = sqoop.command()

        # Boolean parameters should appear as flags without values
        self.assertIn('--hive-import ', cmd)
        self.assertIn('--hive-overwrite ', cmd)
        self.assertIn('--as-textfile ', cmd)
        self.assertIn('--delete-target-dir ', cmd)
        self.assertIn('--direct ', cmd)

    def test_file_format_parameters(self):
        """Test different file format parameters"""

        # Test Parquet format
        sqoop_parquet = Sqoop(table='test', parquetfile=True)
        parquet_cmd = sqoop_parquet.command()
        self.assertIn('--as-parquetfile', parquet_cmd)

        # Test Avro format
        sqoop_avro = Sqoop(table='test', avrofile=True)
        avro_cmd = sqoop_avro.command()
        self.assertIn('--as-avrodatafile', avro_cmd)


class TestSqoopJob(unittest.TestCase):
    """Test cases for SqoopJob class"""

    def test_sqoop_job_initialization(self):
        """Test SqoopJob object initialization"""

        job = SqoopJob()
        self.assertIsInstance(job.priority_options, list)
        self.assertIsInstance(job._properties, dict)

        # Test with job_id parameter
        job_with_id = SqoopJob(job_id='test_job_123')
        self.assertIsInstance(job_with_id.priority_options, list)
        self.assertIsInstance(job_with_id._properties, dict)

    def test_list_running_jobs_method_exists(self):
        """Test that list_runing_jobs static method exists and is callable"""

        # Test method exists
        self.assertTrue(hasattr(SqoopJob, 'list_runing_jobs'))
        self.assertTrue(callable(SqoopJob.list_runing_jobs))

        # Test it's a static method (can be called without instance)
        try:
            # This will likely fail because sqoop is not installed, but shouldn't raise AttributeError
            SqoopJob.list_runing_jobs()
        except Exception as e:
            # Should not be AttributeError or NameError
            self.assertNotIsInstance(e, AttributeError)
            self.assertNotIsInstance(e, NameError)


class TestMapredJob(unittest.TestCase):
    """Test cases for MapredJob class"""

    def test_mapred_job_initialization(self):
        """Test MapredJob object initialization"""

        job = MapredJob()

        # Test priority options are properly initialized
        expected_priorities = ['VERY_HIGH', 'HIGH', 'NORMAL', 'LOW', 'VERY_LOW', 'DEFAULT']
        self.assertEqual(job.priority_options, expected_priorities)
        self.assertIsInstance(job._properties, dict)

        # Test with job_id parameter
        job_with_id = MapredJob(job_id='job_12345')
        self.assertEqual(job_with_id.priority_options, expected_priorities)

    def test_list_running_jobs_method_exists(self):
        """Test that list_runing_jobs static method exists and is callable"""

        # Test method exists
        self.assertTrue(hasattr(MapredJob, 'list_runing_jobs'))
        self.assertTrue(callable(MapredJob.list_runing_jobs))

        # Test it's a static method
        try:
            MapredJob.list_runing_jobs()
        except Exception as e:
            # Should not be AttributeError or NameError
            self.assertNotIsInstance(e, AttributeError)
            self.assertNotIsInstance(e, NameError)

    def test_set_priority_method(self):
        """Test set_priority method functionality"""

        job = MapredJob()

        # Test with valid priority
        result = job.set_priority('job_123', 'HIGH')
        # Method should execute without AttributeError/NameError
        # Return value depends on whether mapred command exists
        self.assertIsInstance(result, bool)

        # Test with invalid priority
        result = job.set_priority('job_123', 'INVALID_PRIORITY')
        self.assertFalse(result)  # Should return False for invalid priority

    def test_priority_validation(self):
        """Test priority validation logic"""

        job = MapredJob()

        # All valid priorities should be accepted by validation logic
        valid_priorities = ['VERY_HIGH', 'HIGH', 'NORMAL', 'LOW', 'VERY_LOW', 'DEFAULT']

        for priority in valid_priorities:
            self.assertIn(priority, job.priority_options)

        # Invalid priorities should not be in the list
        invalid_priorities = ['INVALID', 'SUPER_HIGH', 'MEDIUM', '']

        for priority in invalid_priorities:
            self.assertNotIn(priority, job.priority_options)


if __name__ == '__main__':
    unittest.main()
