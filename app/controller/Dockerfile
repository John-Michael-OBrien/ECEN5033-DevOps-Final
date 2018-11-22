# John-Michael O'Brien
# 11/21/2018
#
# Builds a web service

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


# Tell Flask where to find our app
ENV FLASK_APP /usr/src/app/app.py
# And set Flask as our startup point.
ENTRYPOINT ["bash", "-c"]
CMD ["flask run --host=0.0.0.0"]

# Lastly, grab the args from outside
ARG PORT=5000

EXPOSE $PORT

# Tell Flask to run on our chosen port
ENV FLASK_RUN_PORT $PORT
