git clone <repo_url>

cd VisitorProject

docker compose up -d

docker exec -i pgvec psql -U postgres visit_db < visit_db.sql

python main.py
