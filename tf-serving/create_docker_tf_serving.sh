MODEL_NAME=ai-doc-v1
SAVED_MODEL_PATH=/tf-serving/model/

# Download the TensorFlow Serving Docker image and repo:
docker pull tensorflow/serving:nightly

# First, run a serving image as a daemon:
docker run -d --name serving_base tensorflow/serving:nightly

# Next, copy your `SavedModel` to the container's model folder:
docker cp $SAVED_MODEL_PATH serving_base:/models/$MODEL_NAME
#docker cp /tf-serving/model/ serving_base:/models/ai-doc-v1

# Now, commit the container that's serving your model:
docker commit --change "ENV MODEL_NAME ${MODEL_NAME}" serving_base $MODEL_NAME
#docker commit --change "ENV MODEL_NAME ai-doc-v1" serving_base ai-doc-v1


# Finally, save the image to a tar file:
docker save $MODEL_NAME -o $MODEL_NAME.tar
#docker save ai-doc-v1 -o ai-doc-v1.tar

# You can now stop `serving_base`:
docker kill serving_base



### rEMOVE ALL IMAGES
#docker rmi $(docker images -a -q)
### stop AND REMOVE ALL CONTAINERS
#docker stop $(docker ps -a -q)
#docker rm $(docker ps -a -q)
