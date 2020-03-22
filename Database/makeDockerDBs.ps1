docker build -t lolbot .
docker create -v /var/lib/postgresql/data --name PostgresData alpine
docker run -p 8000:5432 --name anongres -e POSTGRES_PASSWORD=- -d --volumes-from PostgresData lolbot
