import cv2
import insightface
import numpy as np

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
    np.save("embeddings/1 (3001).npy", embedding)
    
else:
    print("No face detected")
