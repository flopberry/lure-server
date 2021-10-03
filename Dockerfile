FROM python:3.9.7-alpine

WORKDIR /code
COPY . /code
RUN apk add gcc musl-dev make g++
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8000
CMD uvicorn __main__:app --reload --workers 1 --host 0.0.0.0 --port 8000