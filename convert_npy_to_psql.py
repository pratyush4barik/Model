import os
import numpy as np
import psycopg2
from pgvector.psycopg2 import register_vector

# ----------------------------
# Database Configuration
# ----------------------------
DB_HOST = "localhost"
DB_NAME = "visit_db"
DB_USER = "postgres"
DB_PASSWORD = "postgres123"
DB_PORT = "55432"

EMBEDDING_FOLDER = "embeddings"

# ----------------------------
# Connect
# ----------------------------
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT
)

register_vector(conn)
cursor = conn.cursor()

files = sorted(
    f for f in os.listdir(EMBEDDING_FOLDER)
    if f.endswith(".npy")
)

print(f"Found {len(files)} embeddings")

for file in files:

    # Use filename (without .npy) as emp_id
    emp_id = os.path.splitext(file)[0]

    embedding = np.load(
        os.path.join(EMBEDDING_FOLDER, file)
    ).astype(np.float32)

    cursor.execute(
        """
        INSERT INTO employee_embeddings (emp_id, embedding)
        VALUES (%s, %s)
        ON CONFLICT (emp_id) DO NOTHING;
        """,
        (emp_id, embedding)
    )

    print(f"Inserted {emp_id}")

conn.commit()
cursor.close()
conn.close()

print("Migration completed successfully!")