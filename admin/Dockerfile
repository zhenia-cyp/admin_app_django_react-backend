FROM python:3.8
LABEL authors="zhenia"
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN pip install  --no-cache-dir -r requirements.txt
COPY . /app

CMD python manage.py runserver 0.0.0.0:8000
