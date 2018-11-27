# John-Michael O'Brien
# 11/21/2018
#
# Builds the dart thrower python program

# Build up a python config with an app in it.
FROM python:3

# From the documentation for the python image (https://hub.docker.com/_/python/),
# we'll copy all of our app over into /usr/src/app
WORKDIR /usr/src/app
# Grab the requirements and get pip to install them
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
# Copy our app files over
COPY . .

# And set Flask as our startup point.
ENTRYPOINT ["bash", "-c"]
CMD ["python3 /usr/src/app/app.py"]
