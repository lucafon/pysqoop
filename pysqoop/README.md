# pysqoop
A python package that lets you sqoop into HDFS data from RDBMS using sqoop.

![PyPI](https://img.shields.io/badge/pip-v.0.0.1-blue.svg)
![PyPI](https://img.shields.io/badge/python-3.5+-brightgreen.svg)

To install the package via pip run 

`
pip install pysqoop
`

You can then use the package using

```
from pysqoop.SqoopImport import Sqoop 
sqoop = Sqoop(help=True)
code = s.perform_import()
```

This will print the output of the command

`
sqoop --help
`

to your stoud e.g.

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