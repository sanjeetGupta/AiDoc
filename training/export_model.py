import t5
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
from constants import TPU_NAME, MODEL_DIR, EXPORTED_MODEL_DIR,EXPORTED_MODEL_BATCH_SIZE

model = t5.models.MtfModel(
    model_dir=MODEL_DIR,
    tpu=TPU_NAME
)
model.batch_size = EXPORTED_MODEL_BATCH_SIZE
model.export(
    export_dir=EXPORTED_MODEL_DIR,
    checkpoint_step=-1,
    beam_size=EXPORTED_MODEL_BEAM_SIZE,
    temperature=EXPORTED_MODEL_TEMPERATURE
)
