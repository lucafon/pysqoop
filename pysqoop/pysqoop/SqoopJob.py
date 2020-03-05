# -*- coding: utf-8 -*-
'''
Author: Luca Fontanili
Date: 2020/03/05
Description: manage sqoop jobs

https://docs.python.org/3.7/library/subprocess.html
'''
import subprocess
import collections


class SqoopJob(object):
    '''class for sqoop job management'''

    def __init__(
            self, job_id=None
    ):
        self.priority_options = []
        self._properties = collections.OrderedDict()

    @staticmethod
    def list_runing_jobs():
        '''List queued jobs if you are using ambari consider visit http://youambariip:8088'''
        command = ["sqoop", "job", "--list"]
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

    sqoop_jobs = SqoopJob()
    sqoop_jobs.list_runing_jobs()
