#!/usr/bin/python3.8

import sys
import os
from jinja2 import Template

import tempfile
import uuid


#import yaml

from kubernetes import client, config
#from kubernetes.client.rest import ApiException
#from kubernetes.client import V1Job, V1VolumeMount, V1NFSVolumeSource

import subprocess
import argparse


TMPL = """
---
apiVersion: batch/v1
kind: Job
metadata:
  name: 'cutvideo-{{job_name}}'
spec:
  backoffLimit: 0
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: cutvideo
        image: rwlove/cutvideo:latest
        command: ["/bin/cutVideo.py", "-f", "{{file_name}}", "-s", "{{start_time}}", "-e", "{{end_time}}", "-p", "{{prefix}}", "-d", "{{target_dir}}" ]
        volumeMounts:
        - name: nfs-brain
          mountPath: /mnt/brain
        - name: nfs-vmheart
          mountPath: /mnt/vmheart
        resources:
          requests:
            memory: 2000Mi
            cpu: 1
          limits:
            memory: 3000Mi
            cpu: 2
      volumes:
      - name: nfs-brain
        nfs:
          # URL for the NFS server
          server: brain.thesteamedcrab.com
          path: /mnt/mass_storage
      - name: nfs-vmheart
        nfs:
          # URL for the NFS server
          server: vmheart.thesteamedcrab.com
          path: /mnt/sda
"""

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
#configuration = client.Configuration()

v1 = client.CoreV1Api()

batch_v1_api = client.BatchV1Api()

#print("Listing pods with their IPs:")
#ret = v1.list_pod_for_all_namespaces(watch=False)
#for i in ret.items:
#    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


parser = argparse.ArgumentParser(description='Cut a Video File')
parser.add_argument('-s', '--start-time', action="store", dest="start_time", required=True)
parser.add_argument('-e', '--end-time', action="store", dest="end_time", required=True)
parser.add_argument('-f', '--file-name', action="store", dest="file_name", required=True)
parser.add_argument('-p', '--prefix', action="store", dest="prefix", required=True)
parser.add_argument('-d', '--target-dir', action="store", dest="target_dir", required=True)
args = parser.parse_args()

in_file = args.file_name
start_time = args.start_time
end_time = args.end_time
prefix = args.prefix
target_dir = args.target_dir

#print("in_file: {}".format(in_file))
#print("target_dir: {}".format(target_dir))
#print("prefix: {}".format(prefix))
#in_name = os.path.basename(in_file)
#out_file = target_dir + "/" + prefix + "/" + in_name

#print("Cutting file: {}, from {} to {} and writing out to {}".format(in_name, start_time, end_time, out_file))

template = Template(TMPL)

job_name = uuid.uuid4().hex

job_txt = template.render(job_name=job_name, file_name=in_file, start_time=start_time, end_time=end_time, prefix=prefix, target_dir=target_dir)

f = tempfile.NamedTemporaryFile()

with open(f.name, 'w') as temp:
    temp.write(job_txt)

subprocess.call(['kubectl', 'apply', '-f', f.name])
