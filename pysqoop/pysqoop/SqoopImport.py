from subprocess import call
import collections


class Sqoop(object):
    _EMPTY_TABLE_AND_QUERY_PARAMETERS_EXCEPTION = '--table or --query is required for import. (Or use sqoop import-all-tables.)\nTry --help for usage instructions.'
    _ALL_EMPTY_PARAMETERS_EXCEPTION = 'all parameters are empty'
    _WRONG_INCREMENTAL_ATTRIBUTE_EXCEPTION = "--incremental needs either 'append' or 'lastmodified'"
    _ERROR_HBASE_KEY_NEEDED = "--hbase-table needs the --hbase-row-key param"
    _ERROR_HBASE_TABLE_NEEDED = "--hbase-row-key needs the --hbase-table param"
    _properties = collections.OrderedDict()
    oracle_partition=None

    def __init__(self, fs=None,create=None, hive_drop_import_delims=None,fields_terminated_by=None,
                 input_escaped_by=None, enclosed_by=None, escaped_by=None, null_string=None,
                 null_non_string=None, table=None, target_dir=None, delete_target_dir=None, connect=None,
                 username=None, password=None, map_colmn_java=None, help=None, query=None, incremental=None,
                 check_column=None, last_value=None, connection_manager=None, connection_param_file=None, driver=None,
                 hadoop_home=None, hadoop_mapred_home=None, metadata_transaction_isolation_level=None, password_alias=None,
                 password_file=None, relaxed_isolation=None, skip_dist_cache=None, temporary_root_dir=None, verbose=None,
                 num_mappers=None, bindir=None, direct=None, parquetfile=None, split_by=None, hive_partition_key=None,
                 hive_partition_value=None , hive_import=None, as_textfile=None, hive_delims_replacement=None, hive_table=None,
                 hive_overwrite=None, warehouse_dir=None, oracle_partition=None, columns=None,
                 hbase_table=None, hbase_row_key=None, m=None
                 ):
        self._properties['-fs'] = fs
        self._properties['--create'] = create
        self._properties['--hive-drop-import-delims'] = hive_drop_import_delims
        self._properties['--fields-terminated-by'] = fields_terminated_by
        self._properties['--input-escaped-by'] = input_escaped_by
        self._properties['--enclosed-by'] = enclosed_by
        self._properties['--escaped-by'] = escaped_by
        self._properties['--null-string'] = null_string
        self._properties['--null-non-string'] = null_non_string
        self._properties['--table'] = table
        self._properties['--target-dir'] = target_dir
        self._properties['--warehouse-dir'] = warehouse_dir
        self._properties['--delete-target-dir'] = delete_target_dir
        self._properties['--connect'] = connect
        self._properties['--username'] = username
        self._properties['--password'] = password
        self._properties['--map-column-java'] = map_colmn_java
        self._properties['--incremental'] = incremental
        self._properties['--check-column'] = check_column
        self._properties['--last-value'] = last_value
        self._properties['--connection-manager'] = connection_manager
        self._properties['--connection-param-file'] = connection_param_file
        self._properties['--driver'] = driver
        self._properties['--hadoop-home'] = hadoop_home
        self._properties['--hadoop-mapred-home'] = hadoop_mapred_home
        self._properties['--metadata-transaction-isolation-level'] = metadata_transaction_isolation_level
        self._properties['--password-alias'] = password_alias
        self._properties['--password-file'] = password_file
        self._properties['--relaxed-isolation'] = relaxed_isolation
        self._properties['--split-by'] = split_by
        self._properties['--hive-table'] = hive_table
        self._properties['--hive-partition-key'] = hive_partition_key
        self._properties['--hive-partition-value'] = hive_partition_value
        self._properties['--skip-dist-cache'] = skip_dist_cache
        self._properties['--temporary-rootdir'] = temporary_root_dir
        self._properties['--verbose'] = verbose
        self._properties['--num-mappers'] = num_mappers
        self._properties['--bindir'] = bindir
        self._properties['--hive-delims-replacement'] = hive_delims_replacement
        self._properties['--columns'] = columns

        #columns for HBase
        self._properties['--hbase-table'] = hbase_table
        self._properties['--hbase-row-key'] = hbase_row_key
        self._properties['-m'] = m
        
        self._command = None
        
        if help:
            self._properties['--help'] = ''
        if hive_import:
            self._properties['--hive-import'] = ''
        if hive_overwrite:
            self._properties['--hive-overwrite'] = ''
        if as_textfile:
            self._properties['--as-textfile'] = ''
        if hive_drop_import_delims:
            self._properties['--hive-drop-import-delims'] = ''
        if delete_target_dir:
            self._properties['--delete-target-dir'] = ''
        if direct:
            self._properties['--direct'] = ''
        if parquetfile:
            self._properties['--as-parquetfile'] = ''
        if oracle_partition:
            self._oracle_partition='-Doraoop.import.partitions={}'.format(oracle_partition)
        self._properties['--query'] = query
        
    def build_command(self)->None:
        self._perform_checks()
        if not self.oracle_partition:
            self._command = \
            'sqoop import {}'.format(
                ' '.join(['{} {}'.format(key, val) for key, val in self._properties.items() if val is not None])
                )
        else:
            self._command = \
            'sqoop import {} {}'.format(
                self.oracle_partition,
                ' '.join(['{} {}'.format(key,val) for key, val in self._properties.items() if val is not None])
                )
    
    def _perform_checks(self):
        if all(v is None for v in self._properties.values()):
            raise Exception(self._ALL_EMPTY_PARAMETERS_EXCEPTION)
        if not self._properties['--table'] and not self._properties['--query'] and '--help' not in self._properties.keys():
            raise Exception(self._EMPTY_TABLE_AND_QUERY_PARAMETERS_EXCEPTION)
        if self._properties['--incremental'] and self._properties['--incremental'] not in ['lastmodified', 'append']:
            raise Exception(self._WRONG_INCREMENTAL_ATTRIBUTE_EXCEPTION)
        if self._properties['--hbase-table'] and not self._properties['--hbase-row-key'] :
            raise Exception(self._ERROR_HBASE_KEY_NEEDED)
        if self._properties['--hbase-row-key'] and not self._properties['--hbase-table'] :
            raise Exception(self._ERROR_HBASE_TABLE_NEEDED)

    def properties(self):
        return self._properties

    def command(self)->str:
        self.build_command()
        return self._command

    def perform_import(self):
        self.build_command()
        try:
            print(self._command)
            return call(self._command, shell=True)
        except Exception as e:
            print(e)
            return 90
    
    def set_param(self, param:str, value:str)->bool:
        if param in self._properties:
            self._properties[param] = value
            return True
        else:
            return False
    
    def unset_param(self, param:str)->bool:
        if param in self._properties:
            self._properties[param] = None
            return True
        else:
            return False
        