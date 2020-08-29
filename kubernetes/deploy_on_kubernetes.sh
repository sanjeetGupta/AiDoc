## create a cluster in GOOGLE KUBERNETES ENGINE using the UI named cluster-1
### FOLLOWING COMMANDS are to be run on the google cloud shell###
## Set cluster-1 as the default cluster for kubectl command
gcloud config set container/cluster cluster-1

## Pass credentials of the cluster to the Kubectl command
gcloud container clusters get-credentials cluster-1 --zone us-central1-c --project orbital-highway-285115

## login to docker hub
docker login

### if using a private docker image, run this to create a "secret" object in kubernetes
kubectl create secret docker-registry regcred --docker-server=https://index.docker.io/v1/ --docker-username=<your-name> --docker-password=<your-pword> --docker-email=<your-email>
##or
kubectl create secret generic regcred \
    --from-file=.dockerconfigjson=.docker/config.json \
    --type=kubernetes.io/dockerconfigjson
###

## create a deployment of the docker image from docker hub
kubectl apply -f deployment.yaml
## create a service
kubectl apply -f service.yaml

## check pods
kubectl get pods

