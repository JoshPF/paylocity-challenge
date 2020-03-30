FROM python:3.7

EXPOSE 8080

RUN pip3 install flask flask_api sqlalchemy flask_sqlalchemy mysqlclient
RUN apt-get -y update; apt-get install -y netcat

#WORKDIR /usr/src
COPY . .

CMD ./wait_for_db.sh
