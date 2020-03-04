# -*- coding: utf-8 -*-
'''
Author: Marco A. Gallegos
Date: 2020/02/03
Description: manage scoop jobs, we going to consider list sqoop jobs,
store sqoop jobs, delete sqoop jobs, cancel running sqoop jobs

https://docs.python.org/3.7/library/subprocess.html
'''
import subprocess
import collections

class SqoopJob(object):
    '''class for sqoop job management'''
    
    def __init__(
            self, job_id=None
    ):
        self._properties = collections.OrderedDict()
    
    @staticmethod
    def list_runing_jobs():
        command=["mapred","job","-list"]
        try:
            process = subprocess.run(
                command, stdout=subprocess.PIPE,
                encoding="utf-8"
                )
            print(process.stdout)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    SqoopJob.list_runing_jobs()
    
    sqoopjobs=SqoopJob()
    sqoopjobs.list_runing_jobs()