# Postgres
FROM postgres:13.2-alpine
COPY /init_multitype_db.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/init_multitype_db.sh
