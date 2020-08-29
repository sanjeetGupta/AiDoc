# Run this to build the image
docker build -f Dockerfile -t ai-doc .
# To check docker images
docker images

# push the image to doceker hub
# login to docker hub
docker login
# get image id of the docker you want to push 6d668ca7e931
docker images
# Tag the Image to the rep\
docker tag 6d668ca7e931 sanjeetgupta/ai-doc:v3
# Push the image to hub
docker push sanjeetgupta/ai-doc:v3

# should run on any machine
# Now test the pushed version, this will get the image from docker hub and run it
docker run --rm -p 8501:8501 sanjeetgupta/ai-doc:v3
