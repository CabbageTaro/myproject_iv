FROM python:3.11
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
WORKDIR /src
ADD requirements.txt /src/
RUN pip3 install -r requirements.txt
ADD . /src/
EXPOSE 8000