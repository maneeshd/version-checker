# Build Image
FROM python:3.7.6-alpine

LABEL maintainer="Maneesh Divana <maneeshd77@gmail.com>"
LABEL description="A slim image to run a FastAPI server using uvicorn/uvloop for version checker"
LABEL version="1.0"

COPY requirements.txt /api

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make \
    && python -m pip install -U -r /api/requirements.txt \
    && apk del .build-deps gcc libc-dev make

COPY server.py /api

WORKDIR /api

EXPOSE 8000

CMD ["uvicorn", "server:api", "--host", "0.0.0.0", "--port", "8000"]