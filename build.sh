#!/bin/bash

buildah build --format=docker -f Dockerfile -t brain:5000/cutvideo .

buildah push --tls-verify=false brain:5000/cutvideo:latest
