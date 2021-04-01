#!/usr/local/bin/python3.8

import sys
import os
import ffmpeg
import argparse

from moviepy.editor import *

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

in_name = os.path.basename(in_file)

out_file = target_dir + "/" + prefix + in_name
if os.path.isfile(out_file):
    out_file = target_dir + "/" + prefix + "-2." + in_name

print("out_file: " + out_file)

clip = VideoFileClip(in_file).subclip(start_time, end_time)
clip.write_videofile(out_file)
