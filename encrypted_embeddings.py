import cv2
import insightface
import numpy as np
from cryptography.fernet import Fernet

#arcface model
app = insightface.app.FaceAnalysis()
app.prepare(ctx_id=-1)

#image location
img = cv2.imread("person1.jpeg")

#detecting faces
faces = app.get(img)

#extract embedding
if len(faces) > 0:
    print("Faces found:", len(faces))
    embedding = faces[0].embedding
    print("Embedding shape:", embedding.shape)
    print(embedding)
    
    #encryption of embedding
    # Generate key once
    key = Fernet.generate_key()
    with open("keys/secret.key", "wb") as f:
        f.write(key)
    
    fernet = Fernet(key)

    # Convert embedding to bytes
    data = embedding.tobytes()

    # Encrypt
    encrypted = fernet.encrypt(data)

    with open("encrypted_emb/emb1.enc", "wb") as f:
        f.write(encrypted)
    
else:
    print("No face detected")
