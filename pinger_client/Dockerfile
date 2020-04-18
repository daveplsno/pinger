FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./data/ping.tsmtemplate ./
COPY ./data/collector.py ./

CMD [ "python", "./collector.py" ]