FROM python:3.9-slim-buster

WORKDIR /src

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./app .

EXPOSE 5431
EXPOSE 5432

CMD python app.py

