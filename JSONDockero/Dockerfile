FROM python:3.6.4
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
ADD . /code/
