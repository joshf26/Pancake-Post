FROM python:3.7.2

COPY ./app /app

RUN pip3 install -r requirements.txt

ENV FLASK_APP "./app/main.py"

CMD ["flask", "run"]
