#!/usr/bin/python3.9

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
        return self.cmd_list.copy()

def getTokenFromCmd(cmd, regex):
    m = re.compile(regex)
    g = m.search(cmd)
    return g.group(1)

###
# Convert a single job to a list
def convertCommandToList(job_name, cmds):
    c = Command()
    c.addJobName(job_name)
        
    job = cmds.decode('ascii').replace('"','').replace('[/bin/cutVideo.py,','').replace(']','')

    tok = getTokenFromCmd(job, '.*-f,(.*?)(?:,.*|$)')
    c.addSourceFile(tok)
    tok = getTokenFromCmd(job, '.*-s,(.*?)(?:,.*|$)')
    c.addStartTime(tok)
    tok = getTokenFromCmd(job, '.*-e,(.*?)(?:,.*|$)')
    c.addEndTime(tok)
    tok = getTokenFromCmd(job, '.*-p,(.*?)(?:,.*|$)')
    c.addPrefix(tok)        
    tok = getTokenFromCmd(job, '.*-d,(.*?)(?:,.*|$)')
    c.addDestDir(tok)

    return c.toList()

###
# Process a single job/command
def getJobAsList(job):
    kubectl_cmd = "kubectl -n default get job %s -o jsonpath='{.spec.template.spec.containers[0].command}'" % job
    cmds = subprocess.check_output(kubectl_cmd, shell=True)
    return convertCommandToList(job, cmds)

def printJobsTable(title, s):
    l = []
    out = subprocess.check_output(s, shell=True)
    if out:
        jobs = list(out.decode('ascii').split(" "))
        for job in jobs:
            j = getJobAsList(job)
            l.append(j)
        print(tabulate(l,headers=[title, "Source", "Destination", "Prefix", "Start", "End"]))
    return len(l)

def printFailedJobsTable():
    return printJobsTable("Failed Job Name", "kubectl get jobs -o=jsonpath='{.items[?(@.status.failed>0)].metadata.name}'")

def printRunningJobsTable():
    return printJobsTable("Running Job Name", "kubectl get jobs -o=jsonpath='{.items[?(@.status.active==1)].metadata.name}'")

def printSuccessfulJobsTable():
    return printJobsTable("Completed Job Name", "kubectl get jobs -o=jsonpath='{.items[?(@.status.succeeded==1)].metadata.name}'")

num_printed = printFailedJobsTable()

if num_printed > 0:
    print()
    
printSuccessfulJobsTable()

if num_printed > 0:
    print()

printRunningJobsTable()
