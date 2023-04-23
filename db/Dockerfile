FROM postgres
#COPY postgres.conf /etc/postgresql/postgresql.conf
COPY db-seed-files/ /docker-entrypoint-initdb.d/
#CMD ["-c", "config_file=/etc/postgresql/postgresql.conf"]
