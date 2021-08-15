# pysqoop
A python package that lets you sqoop into HDFS/Hive/HBase data from RDBMS using sqoop.

[![PyPI](https://img.shields.io/badge/pip-v.0.0.16-blue.svg)](https://pypi.org/project/pysqoop)
![Python](https://img.shields.io/badge/python-3.5+-green.svg)
[![Tests](https://img.shields.io/badge/tests-6%20%2F%206-brightgreen.svg)](https://github.com/lucafon/pysqoop/blob/master/unittests/unintary_tests.py)
[![MIT license](http://img.shields.io/badge/license-MIT-orange.svg)](http://opensource.org/licenses/MIT)

To install the package via pip, run 

`
pip install pysqoop
`

You can then use the package using

```python
from pysqoop.SqoopImport import Sqoop 
sqoop = Sqoop(help=True)
code = sqoop.perform_import()
```

This will print the output of the command

`
sqoop --help
`

to your stoud; e.g.

```
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/usr/hdp/2.6.3.0-235/hadoop/lib/slf4j-log4j12-1.7.10.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/usr/hdp/2.6.3.0-235/accumulo/lib/slf4j-log4j12.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.slf4j.impl.Log4jLoggerFactory]
18/08/13 20:25:13 INFO sqoop.Sqoop: Running Sqoop version: 1.4.6.2.6.3.0-235
usage: sqoop import [GENERIC-ARGS] [TOOL-ARGS]

Common arguments:
   --connect <jdbc-uri>                                       Specify JDBC
                                                              connect
                                                              string
   --connection-manager <class-name>                          Specify
                                                              connection
                                                              manager
                                                              class name
   ...
```

#### Useful Resources

* HBase Client for Python : [happybase](https://github.com/python-happybase/happybase/blob/master/doc/index.rst)


#### A more concrete example
The following code
```python
sqoop = Sqoop(fs='hdfs://remote-cluster:8020', hive_drop_import_delims=True, fields_terminated_by='\;',
enclosed_by='\'"\'', escaped_by='\\\\', null_string='\'\'', null_non_string='\'\'',
table='sample_table', target_dir='hdfs://remote-cluster/user/hive/warehouse/db/sample_table',
delete_target_dir=True, connect='jdbc:oracle:thin:@//your_ip:your_port/your_schema',
username='user', password='pwd', num_mappers=2,
bindir='/path/to/bindir/folder')

sqoop.perform_import()
```

will execute the following command

`
sqoop import -fs hdfs://remote-cluster:8020 --hive-drop-import-delims  --fields-terminated-by \; --enclosed-by \'\"\' --escaped-by \\\\ --null-string \'\' --null-non-string \'\' --table sample_table --target-dir hdfs://remote-cluster/user/hive/warehouse/db/sample_table --delete-target-dir  --connect jdbc:oracle:thin:@//your_ip:your_port/your_schema --username user --password pwd --num-mappers 2 --bindir /path/to/bindir/folder
`

#### Conditional Building

Use the `set_param`, `unset_param` function to build conditioned sqoop imports.

```python

sqoop = Sqoop(table="MyTable")

sqoop.set_param(param="--connect", value="jdbc:a_valid_string")

if taget_is_hbase :
   added_table = sqoop.set_param(param="--hbase-table", value="MyTable")
   added_key = sqoop.set_param(param="--hbase-row-key", value="Id_MyTable")
   if added_table and added_key:
      print("all params added :D")

sqoop.perform_import()
```

### Unit Testing

In order to run unit tests open the terminal and change the current directory to `unittests` folder.

Then, simply run `python unintary_tests.py`. Add your unit tests in this file



### Doing

* handle sqoop jobs


### TODOs

* add missing parameters
* more tests coverage
