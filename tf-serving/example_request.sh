curl -d '{"inputs": ["nq question: what is the most populous country?"]}' -X POST http://localhost:8501/v1/models/$MODEL_NAME:predict
curl -d '{"inputs": ["nq question: what is the most populous country?"]}' -X POST http://localhost:8501/v1/models/ai-doc-v1:predict
