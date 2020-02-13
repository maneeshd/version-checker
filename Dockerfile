# Build Image
FROM python:3.7.6-alpine

LABEL maintainer="Maneesh Divana <maneeshd77@gmail.com>"
LABEL description="A slim image to run a FastAPI server using gunicorn with uvicorn/uvloop worker class"
LABEL version="1.0"

COPY requirements.txt server.py /api/

WORKDIR /api

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make \
    && python -m pip install -U -r requirements.txt \
    && apk del .build-deps gcc libc-dev make

EXPOSE 8000

CMD ["uvicorn", "server:api", "--host", "0.0.0.0", "--port", "8000"]