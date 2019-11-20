from subprocess import call
import collections


class Sqoop():
    _EMPTY_TABLE_AND_QUERY_PARAMETERS_EXCEPTION = '--table or --query is required for import. (Or use sqoop import-all-tables.)\nTry --help for usage instructions.'
    _ALL_EMPTY_PARAMETERS_EXCEPTION = 'all parameters are empty'
    _WRONG_INCREMENTAL_ATTRIBUTE_EXCEPTION = "--incremental needs either 'append' or 'lastmodified'"
    _properties = collections.OrderedDict()

    def __init__(self, fs=None,create=None, hive_drop_import_delims=None,fields_terminated_by=None, input_escaped_by=None, enclosed_by=None, escaped_by=None,
                 null_string=None, null_non_string=None, table=None, target_dir=None, delete_target_dir=None, connect=None,
                 username=None, password=None, map_colmn_java=None, help=None, query=None, incremental=None,
                 check_column=None, last_value=None, connection_manager=None, connection_param_file=None, driver=None,
                 hadoop_home=None, hadoop_mapred_home=None, metadata_transaction_isolation_level=None, password_alias=None,
                 password_file=None, relaxed_isolation=None, skip_dist_cache=None, temporary_root_dir=None, verbose=None,
                 num_mappers=None, bindir=None, direct=None, parquetfile=None, split_by=None, hive_partition_key=None,
                 hive_partition_value=None , hive_import=None, as_textfile=None, hive_delims_replacement=None, hive_table=None,
                 hive_overwrite=None, warehouse_dir=None):
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
        self._properties['--query'] = query
        self._perform_checks()
        self._coomand = 'sqoop import {}'.format(
            ' '.join(['{} {}'.format(key, val) for key, val in self._properties.items() if val is not None]))

    def _perform_checks(self):
        if all(v is None for v in self._properties.values()):
            raise Exception(self._ALL_EMPTY_PARAMETERS_EXCEPTION)
        if not self._properties['--table'] and not self._properties['--query'] and '--help' not in self._properties.keys():
            raise Exception(self._EMPTY_TABLE_AND_QUERY_PARAMETERS_EXCEPTION)
        if self._properties['--incremental'] and self._properties['--incremental'] not in ['lastmodified', 'append']:
            raise Exception(self._WRONG_INCREMENTAL_ATTRIBUTE_EXCEPTION)

    def properties(self):
        return self._properties

    def command(self):
        return self._coomand

    def perform_import(self):
        try:
            print(self._coomand)
            return call(self._coomand, shell=True)
        except Exception as e:
            print(e)
            return 90

