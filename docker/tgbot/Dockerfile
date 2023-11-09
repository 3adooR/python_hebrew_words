FROM python:3.10-alpine
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt --no-cache-dir
COPY . /app
RUN apk update && apk add bash
CMD python app.py