FROM ubuntu:16.04

MAINTAINER Grigorev Pavel

# Обвновление списка пакетов
RUN apt-get -y update

#
# Установка postgresql
#
ENV PGVER 9.5
RUN apt-get install -y postgresql-$PGVER

# Установка Python3
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install pytz
RUN pip3 install psycopg2
RUN pip3 install gunicorn
RUN pip3 install flask
RUN pip3 install jsonify

USER postgres

# Create a PostgreSQL role named ``pavel`` with ``lomogi99`` as the password and
# then create a database `students` owned by the ``docker`` role.
RUN /etc/init.d/postgresql start &&\
    psql -c "CREATE DATABASE forums WITH template=template0 encoding='UTF8';" &&\
    psql --command "CREATE USER pavel WITH PASSWORD 'lomogi99';" &&\
    psql -c "grant all privileges on database forums to pavel;" &&\
    psql -d "forums" -c "CREATE EXTENSION CITEXT;" &&\
    psql -c "SELECT * FROM pg_collation;" &&\
    /etc/init.d/postgresql stop

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
RUN echo "host all  all    0.0.0.0/0  trust" >> /etc/postgresql/$PGVER/main/pg_hba.conf
RUN echo "local all all trust" >> /etc/postgresql/$PGVER/main/pg_hba.conf
RUN echo "host  all all 127.0.0.1/32 trust" >> /etc/postgresql/$PGVER/main/pg_hba.conf
RUN echo "host  all all ::1/128 trust" >> /etc/postgresql/$PGVER/main/pg_hba.conf

RUN echo "listen_addresses='*'" >> /etc/postgresql/$PGVER/main/postgresql.conf
RUN echo "synchronous_commit=off" >> /etc/postgresql/$PGVER/main/postgresql.conf

# Expose the PostgreSQL port
EXPOSE 5432

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# Back to the root user
USER root

# Копируем исходный код в Docker-контейнер
ENV WORK /opt/db_tp
ADD api/ $WORK/api/
ADD enquiry/ $WORK/enquiry/
ADD db.py $WORK/db.py
ADD my_db.sql $WORK/my_db.sql

# Объявлем порт сервера
EXPOSE 5000

#
# Запускаем PostgreSQL и сервер
#
ENV PGPASSWORD lomogi99
CMD service postgresql start &&\
    cd $WORK/ &&\
    psql -h localhost -U pavel -d forums -f my_db.sql &&\
    gunicorn -w 9 -k sync --worker-connections 18 -t 360 -b :5000 db:app


#docker build -t grigorev .
#docker run -p 5000:5000 --name grigorev -t grigorev
#docker rm -f $(docker ps -a -q)
