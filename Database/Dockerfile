FROM postgres:11

ADD CreateDB.sql /docker-entrypoint-initdb.d/
ADD CreateTables.sql /docker-entrypoint-initdb.d/

EXPOSE 8000