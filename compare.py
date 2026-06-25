import cv2
import numpy as np
import psycopg2
from pgvector.psycopg2 import register_vector
from insightface.app import FaceAnalysis

# ----------------------------
# Database Configuration
# ----------------------------
conn = psycopg2.connect(
    host="localhost",
    database="visit_db",
    user="postgres",
    password="postgres123",
    port="55432"
)

register_vector(conn)
cursor = conn.cursor()

# ----------------------------
# Load ArcFace
# ----------------------------
app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=-1)   # CPU

# ----------------------------
# Load query image
# ----------------------------
image_path = "image.png"

img = cv2.imread(image_path)
faces = app.get(img)

if len(faces) == 0:
    print("No face detected!")
    exit()

embedding = faces[0].embedding.astype(np.float32)

# ----------------------------
# Search nearest embedding
# ----------------------------
cursor.execute(
    """
    SELECT
        emp_id,
        embedding <=> %s AS distance
    FROM employee_embeddings
    ORDER BY embedding <=> %s
    LIMIT 1;
    """,
    (embedding, embedding)
)

result = cursor.fetchone()

if result:
    visitor_id, distance = result

    print(f"Matched Visitor : {visitor_id}")
    print(f"Cosine Distance : {distance:.6f}")

    # Threshold (adjust after testing)
    if distance < 0.35:
        print("✅ Face Verified")
    else:
        print("❌ Unknown Person")

cursor.close()
conn.close()