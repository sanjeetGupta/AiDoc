MODEL_NAME=ai-doc-v1
docker run -t --rm -p 8501:8501 --name $MODEL_NAME-server $MODEL_NAME &
#docker run -t --rm -p 8501:8501 --name ai-doc-v1-server ai-doc-v1 &
#docker stop ai-doc-v1-server

