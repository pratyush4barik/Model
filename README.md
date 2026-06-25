git clone https://github.com/pratyush4barik/Model.git

docker compose up -d

docker exec -i pgvec psql -U postgres visit_db < visit_db.sql

python compare.py

# insatll docker desktop
# instal postgreSQL (pgAdmin4)
