FROM python:3.10

COPY ./requirements.txt /www/requirements.txt
RUN pip install -r /www/requirements.txt

COPY . /www
WORKDIR /www

EXPOSE 8000
EXPOSE 5555