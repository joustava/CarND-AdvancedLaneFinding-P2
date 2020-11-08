FROM python:3.8

ENV PYTHONPATH=/app


RUN apt-get update
RUN apt-get install \
  'clang' \
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
COPY alf alf
COPY setup.py .


RUN cd /usr/local/lib/python3.8/site-packages && python /app/setup.py develop

# command to run on container start
CMD [ "python", "./alf/processor.py" ]