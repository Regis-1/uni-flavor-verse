FROM postgres:16.2-alpine
COPY tables.sql /docker-entrypoint-initdb.d/
RUN mkdir -p /db_data
COPY *.csv /db_data/
EXPOSE 5432
