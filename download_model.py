import insightface

app = insightface.app.FaceAnalysis()
app.prepare(ctx_id=-1)
print("Models downloaded successfully")