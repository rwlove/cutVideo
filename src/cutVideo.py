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

if not os.path.isfile(in_file):
    print(in_file + " is not a valid file.")
    sys.exit(os.EX_OSFILE)

if not os.path.isdir(target_dir):
    print(target_dir + "is not a valid directory.")
    sys.exit(os.EX_OSFILE)

def findNextNumberOutfile(f):
    import re

    print("Checking if \'" + f + "\' is a file")
    if not os.path.isfile(f):
        print("\'" + f + "\' is not a file")
        print("returning: " + f)
        return f

    m = re.search(r'(?:[/ ]){prefix}-(.*)-(\d+)\..*', f)
    if not m:
        print("Could not find a number")
        print("returning: " + f)
        return f

    print("Number is " + str(m) + ".")
    print(m.group(1))
    num = int(m.group(1))
    num += 1

    basename = os.path.splitext(in_name)[0]
    extension = os.path.splitext(in_name)[1]
    f2 = target_dir + "/" + prefix + "-" + basename + "-" + str(num) + extension

    print("Checking if \'" + f2 + "\' is a file")
    if not os.path.isfile(f2):
        print("\'" + f2 + "\' is not a file")
        print("returning: " + f2)
        return f2
    else:
        return findNextNumberOutfile(f2)

basename = os.path.splitext(in_name)[0]
extension = os.path.splitext(in_name)[1]
f = target_dir + "/" + prefix + "-" + basename + "-1" + extension

print("in_name: " + in_name)
print("basename: " + basename)
print("extension: " + extension)
print("f: " + f)

out_file = findNextNumberOutfile(f)
print("out_file (final): " + out_file)

clip = VideoFileClip(in_file).subclip(start_time, end_time)
clip.write_videofile(out_file)

sys.exit(os.EX_OK)
