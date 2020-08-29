# get image id of the docker you want to push 6d668ca7e931
docker images

# login to docker hub
docker login

# Tag the Image to the rep\
docker tag 6d668ca7e931 sanjeetgupta/ai-doc:v3

# Push the image to hub
docker push sanjeetgupta/ai-doc:v3

