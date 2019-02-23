FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./ /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt
