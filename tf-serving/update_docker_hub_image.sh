MODEL_NAME=ai-doc-v1
SAVED_MODEL_PATH=/tf-serving/model/

#Download the ai-doc-v1 image from dockerhub repo:
docker pull sanjeetgupta/ai-doc-v1:latest


# First, run a serving image as a daemon:
docker run -d --name ai-doc-v1 sanjeetgupta/ai-doc-v1:latest

# check the list of images
docker images

docker ps

# Next, copy your  New SavedModel to the container's model folder:
docker cp $SAVED_MODEL_PATH ai-doc-v1:/models/$MODEL_NAME
#docker cp tf-serving/model/ ai-doc-v1:/models/ai-doc-v1

# Now, commit the container that's serving your model:
docker commit --change "ENV MODEL_NAME ${MODEL_NAME}" serving_base $MODEL_NAME
#docker commit --change "ENV MODEL_NAME ai-doc-v1" ai-doc-v1 ai-doc-v1


