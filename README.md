# Version Checker
REST API to check given two softawre version numbers, if the 1st number is ***before***, ***after*** or ***equal*** to the 2nd number.

## Problem Statement

**Version Checker:**

**Please write a web service that takes in two strings and returns a string indicating if the first string is before, after, or equal to the second string. Where "before", "after" and "equal" are based interpretation as software version numbers.**

Examples:

1.0.0 is "before" 1.0.1

2.0 is "after" 1.0.0

## Solution

I have used **[FastAPI](https://fastapi.tiangolo.com/)** to create the REST API web service. This framework offers asynchronous code running and is based on [ASGI](https://asgi.readthedocs.io/en/latest/) and in-built API documentation generator.

## Requirements

- [Python](https://www.python.org/downloads/release/python-376/) >= `3.6.8` (`3.7.6` recommended)
- Python Packages [requirements.txt](requirements.txt)
- [Docker](https://www.docker.com/products/docker-desktop) (if running the docker image)

## Running the app

- Install the python packages

```bash
$ python -m pip install -r requirements.txt -U
```

- Start server

```bash
$ cd version-checker

$ python -m uvicorn --host "0.0.0.0" --port 8000 server:api
```

- The server is now live @ http://localhost:8000/

**Assuming port `8000` is open. If not please change the port to an open port (8080, 8081..etc) in the above command.*

## API Endpoints

**Endpoint: http://localhost:8000/api/v1/version_checker?ver_1=<version_number_1>&ver_2=<version_number_2>***

**Method  : `GET`**

## Examples

**Request : `GET` http://localhost:8000/api/v1/version_checker?ver_1=1.0.0&ver_2=1.0.1**

**Response: `JSON` `{"result": "1.0.0 is before 1.0.1"}`**


**Request : `GET` http://localhost:8000/api/v1/version_checker?ver_1=2.0&ver_2=1.0.1**

**Response: `JSON` `{"result": "2.0 is after 1.0.1"}`**


**Request : `GET` http://localhost:8000/api/v1/version_checker?ver_1=2.0&ver_2=2.0**

**Response: `JSON` `{"result": "2.0 is equal to 2.0"}`**

## Docker Image

The docker image can also be used to run the api

DockerHub Image: https://hub.docker.com/r/maneeshd/version_checker

- Pull and run the docker image:

```bash
$ docker pull maneeshd/version_checker:latest

$ docker run --rm --name version_checker -p 8000:8000 maneeshd/version_checker:latest
```

- Stop the docker image after use:

Ctrl + C can be pressed to kill the server or in a new terminal execute

```bash
$ docker rm -f version_checker
```

## Author

**Maneesh Divana | [maneeshd77@Gmail.com](mailto:maneeshd77@gmail.com)**

## Flask-Restful Version

There is also a [Flask-Restful](https://flask-restful.readthedocs.io/en/latest/) version of the api and a corresponding docker image.

The API Endpoints, paths and query string format are the same as above.

**Running this verison of the api:**

```bash
$ python -m pip install -U flask-restful

$ cd version-checker

$ python flask_server.py
```

**Docker Image:**

DockerHub: https://hub.docker.com/r/maneeshd/version_checker_flask

```bash
$ docker pull maneeshd/version_checker_flask:latest

$ docker run --rm --name version_checker_flask -p 8000:8000 maneeshd/version_checker_flask:latest
```
