#!/usr/bin/python3.8

import sys
import os
import subprocess
import re
from tabulate import tabulate

class Command:
    cmd_list = [None] * 6

    def addJobName(self, j):
        self.cmd_list[0] = j

    def addSourceFile(self, f):
        self.cmd_list[1] = f

    def addDestDir(self, d):
        self.cmd_list[2] = d

    def addPrefix(self, p):
        self.cmd_list[3] = p

    def addStartTime(self, s):
        self.cmd_list[4] = s

    def addEndTime(self, e):
        self.cmd_list[5] = e

    def toList(self):
        return self.cmd_list

def convertCommandToList(job_name, cmds):
    c = Command()
    cmd_list = list(cmds.decode('ascii').split(" "))
    for job_cmd in cmd_list:
        job = job_cmd.replace('"','').replace('[/bin/cutVideo.py,','').replace(']','')
        fs = re.compile('.*-f,(.*?)(?:,.*|$)')
        ss = re.compile('.*-s,(.*?)(?:,.*|$)')
        es = re.compile('.*-e,(.*?)(?:,.*|$)')
        ps = re.compile('.*-p,(.*?)(?:,.*|$)')
        ds = re.compile('.*-d,(.*?)(?:,.*|$)')
        g = fs.search(job)
        c.addSourceFile(g.group(1))
        g = ss.search(job)
        c.addStartTime(g.group(1))
        g = es.search(job)
        c.addEndTime(g.group(1))
        g = ps.search(job)
        c.addPrefix(g.group(1))
        g = ds.search(job)
        c.addDestDir(g.group(1))
        c.addJobName(job_name)
    return c

def getJobAsList(job):
    kubectl_cmd = "kubectl -n default get job %s -o jsonpath='{.spec.template.spec.containers[0].command}'" % job
    cmds = subprocess.check_output(kubectl_cmd, shell=True)
    c = convertCommandToList(job, cmds)
    return c.toList()

def printJobsTable(title, s):
    out = subprocess.check_output(s, shell=True)
    if out:
        jobs = list(out.decode('ascii').split(" "))
        l = []
        for job_cmd in jobs:
            l.append(getJobAsList(job_cmd))
        print(tabulate(l,headers=[title, "Source", "Destination", "Prefix", "Start", "End"]))

def printFailedJobsTable():
    printJobsTable("Failed Job Name", "kubectl get jobs -o=jsonpath='{.items[?(@.status.failed>0)].metadata.name}'")

def printRunningJobsTable():
    printJobsTable("Running Job Name", "kubectl get jobs -o=jsonpath='{.items[?(@.status.active==1)].metadata.name}'")

printFailedJobsTable()
printRunningJobsTable()
