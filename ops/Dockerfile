FROM python:3.8

RUN apt-get update ##[edited]
RUN apt-get install \
  'ffmpeg' \
  'libsm6' \ 
  'libxext6' -y

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt .
# COPY setup.py .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ ./

# command to run on container start
CMD [ "python", "./alf/classifier.py" ]