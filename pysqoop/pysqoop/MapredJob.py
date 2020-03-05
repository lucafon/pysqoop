# -*- coding: utf-8 -*-
'''
Author: Marco A. Gallegos
Date: 2020/02/03
Description: manage mapred jobs, we going to consider list sqoop jobs,
store sqoop jobs, delete sqoop jobs, cancel running sqoop jobs

https://docs.python.org/3.7/library/subprocess.html
'''
import subprocess
import collections


class MapredJob(object):
    '''class for sqoop job management'''

    def __init__(self, job_id=None):
        self.priority_options = []
        self._properties = collections.OrderedDict()

    @staticmethod
    def list_runing_jobs():
        '''List queued jobs if you are using ambari consider visit http://youambariip:8088'''
        command = ["mapred", "job", "-list"]
        try:
            process = subprocess.run(
                command, stdout=subprocess.PIPE,
                encoding="utf-8"
            )
            print(process.stdout)
        except Exception as e:
            print(e)

    def set_priority(self, job_id: str, priority: str) -> bool:
        '''change priority of a runing job VERY_HIGH HIGH NORMAL LOW VERY_LOW DEFAULT'''
        command = f"mapred job -set-priority {job_id} {priority}"
        if priority in self._priority_options:
            try:
                process = subprocess.run(
                    command, stdout=subprocess.PIPE,
                    encoding="utf-8"
                )
                print(process.stdout)
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False


if __name__ == "__main__":
    MapredJob.list_runing_jobs()

    mapred_jobs = MapredJob()
    mapred_jobs.list_runing_jobs()
