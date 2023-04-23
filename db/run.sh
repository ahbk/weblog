#!/bin/sh
sudo docker run -d --name mypostgres -p 5432:5432 -e POSTGRES_PASSWORD=asdf -v postgres:/var/lib/postgresql/data postgres
