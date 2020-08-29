# AI DOC
Text-to-Text transformer to answer health questions. 
The same model also classifies the question, extracts the symptoms and suggests the speciality of the doctor.
Try it at <a href='sanjeetgupta.com'>sanjeetgupta.com</a>

* Data used has been scraped from multiple health websites on the internet.
* A total of about 7 lakh questions and answers have been scraped.

This repository consists the following code:
* data_prep/ -- Data analysis, cleaning and preparation.
* training/ -- T5 model training and exporting.
* dockerization/ -- containerizing the model with inference running on a flask service.
* tf-serving/ -- containerizing the model using tf-serving base image.
* kubernetes/ -- .yaml files to deploy the container on to a kubernetes cluster on Google Cloud.
* front-end/ -- angular app to build the UI
* cors_proxy_server/ -- proxy server between backend (Kubernetes Service) and Frontend (Angular)

 
 
## Data Preperation 
code in <b>data-prep/<b>

<i><b>data_prep.ipynb</b></i>
* Merges similar Specialities into a single category.
* Removes advertisements from the answers.
* Removes names and locations from the data set.
* Filters the samples based of length, so that the text doesn't surpass the sequence length of the model.
* Creates the input text and output text for the T5 model using tags described below.
* Outputs a file of format below.
```
<question>\t<answer>
```
question example:
```
a_t 24 g_t F q_t My aunt's 4 or 5 bone of spinal cord has increased. So how it will medicate or any surgery required please help with this?
```
answer example:
```
cat_t bone-muscle-problems spc_t Orthopedist sym_t Spinal cord bone increase ans_t Need to have a complete history, with your history it doesn't look that serious but can proceed to weakness of lower limbs if not treated properly.
```

#### Input Tags :
* a_t : age
* g_t : gender
* q_t : question 

#### Output Tags :
* cat_t : Category 
* spc_t : Speciality
* sym_t : Symptom Summary
* ans_t : Doctor's Reply


## Model Training and Exporting. 
code in training/

<i><b>fine_tune.py</b></i>
* Trains a T5 Small model on a TPU. The model has (60M parameters) gs://t5-data/pretrained_models/small
* Sequence lengths of (128,256) i.e. 128 for question and 256 for answer.
* Batch size of 256.
* Epoch = 1

<i><b>export_model.py</b></i>
* Export a checkpoint to a tf exported model format.
* The exported model performs inference(text generation) with a temperature of 1.  


## Containerisation

### Dockerization
code in dockerization/
* app.py to run a Inference flask service.
* Dockerfile to define the image.
* build_run_push.sh consists commands to build, push and run the docker image

### TF serving
code in tf-serving/

* create_docker_tf_serving.sh to create a docker image with tf-serving base image.

I tried both of the above options and decided to use the simple container instead of tf-serving because of performance issues.


## Kubernetes
code in kubernetes/

* deployment.yaml to define the deployment details( like number of pod , docker image name , docker hub credentials). 
* service.yaml to define a LoadBalancer service for the deployment.

## FrontEnd
code in front-end/

* Angular app. 


