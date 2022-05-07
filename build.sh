#!/bin/bash

buildah build --format=docker -f Dockerfile -t brain:5000/cutVideo .

buildah push --tls-verify=false brain:5000/cutvideo:latest
