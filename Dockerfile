# set base image (host OS)
FROM python:3.8

RUN pip install moviepy

# set the working directory in the container

RUN mkdir -p /mnt/vmheart /mnt/brain

WORKDIR /mnt

# copy the dependencies file to the working directory
#COPY requirements.txt .

# install dependencies
#RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/cutVideo.py /bin/cutVideo.py

# command to run on container start
CMD [ "/bin/cutVideo.py", "--help" ]
