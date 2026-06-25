import os
import cv2
import numpy as np
import insightface

# -----------------------------
# Load ArcFace
# -----------------------------
app = insightface.app.FaceAnalysis()
app.prepare(ctx_id=-1)

# -----------------------------
# Input Image
# -----------------------------
test_image = "person2.jpeg"

img = cv2.imread(test_image)

if img is None:
    print("Cannot read image")
    exit()

# -----------------------------
# Detect Face
# -----------------------------
faces = app.get(img)

if len(faces) == 0:
    print("No face detected")
    exit()

print("Face detected")

query_embedding = faces[0].embedding

# -----------------------------
# Search Database
# -----------------------------
embedding_folder = "embeddings"

best_match = None
best_score = -1

for file in os.listdir(embedding_folder):

    if not file.endswith(".npy"):
        continue

    emb_path = os.path.join(embedding_folder, file)

    stored_embedding = np.load(emb_path)

    # Cosine Similarity
    score = np.dot(
        query_embedding,
        stored_embedding
    ) / (
        np.linalg.norm(query_embedding)
        * np.linalg.norm(stored_embedding)
    )

    if score > best_score:
        best_score = score
        best_match = file

# -----------------------------
# Result
# -----------------------------
print("\nBest Match Found")
print("Embedding File :", best_match)
print("Similarity     :", round(float(best_score), 4))

# Threshold
THRESHOLD = 0.6

if best_score >= THRESHOLD:
    print("Person Verified")
else:
    print("Unknown Person")