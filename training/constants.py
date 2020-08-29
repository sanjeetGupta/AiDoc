
## GOOGLE CLOUD PLATFORM
TPU_NAME='' ## TPU NAME
MODEL_DIR = '' ##GCP STORAGE MODEL_DIR
DATA_DIR = ''## GCP STORAGE DATA_DIR
ZONE='' ## TPU ZONE
PROJECT='' ## GCP project name
TPU_TOPOLOGY = "2x2"


## T% pretrained model path
BASE_PRETRAINED_DIR = "gs://t5-data/pretrained_models"


## MODEL EXPORT
EXPORTED_MODEL_CHECKPOINT = -1 ## Model checkpoint to be used -1 => the final checkpoint
EXPORTED_MODEL_DIR = "model" ## EXPORTED MODEL DIR

## The Inference Parameters need to be set while exporting the model these can't be changed once the model is exported.  
EXPORTED_MODEL_BATCH_SIZE = 1 ## BATCH SIZE
EXPORTED_MODEL_BEAM_SIZE = 1 ## Beam Size
EXPORTED_MODEL_TEMPERATURE = 1## temperature
