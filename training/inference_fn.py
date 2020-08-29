import t5
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import os
import tensorflow_text
from time import time
from constants import TPU_NAME, MODEL_DIR, EXPORTED_MODEL_DIR,EXPORTED_MODEL_BATCH_SIZE



def predict_from_mtf_model():
    """
    Works Only with TPU
    """
    checkpoint = -1
    temp_predict = 'inputs.txt'
    temp_out = 'prediction_output'
    model = t5.models.MtfModel(
        model_dir=MODEL_DIR,
        tpu=TPU_NAME
    )

    model.batch_size = 16
    model.predict(
        input_file=temp_predict,
        output_file=temp_out,
        checkpoint_steps=checkpoint,
    )
    ## Print results
    pred_file = list(filter(lambda x: temp_out in x, os.listdir(os.getcwd())))[0]
    with open(pred_file, 'r') as f:
        out_str = f.readlines()
    for o in out_str: print(o)


def load_predict_fn_exported(model_path):
  if tf.executing_eagerly():
    print("Loading SavedModel in eager mode.")
    imported = tf.saved_model.load(model_path, ["serve"])
    return lambda x: imported.signatures['serving_default'](tf.constant(x))['outputs'].numpy()
  else:
    print("Loading SavedModel in tf 1.x graph mode.")
    tf.compat.v1.reset_default_graph()
    sess = tf.compat.v1.Session()
    meta_graph_def = tf.compat.v1.saved_model.load(sess, ["serve"], model_path)
    signature_def = meta_graph_def.signature_def["serving_default"]
    return lambda x: sess.run(
        fetches=signature_def.outputs["outputs"].name,
        feed_dict={signature_def.inputs["input"].name: x}
    )

def answer(question):
    return [ans.decode('utf-8') for ans in predict_fn( [question] * EXPORTED_MODEL_BATCH_SIZE)]



exported_model_path = EXPORTED_MODEL_DIR + '/3/'
start =time()
predict_fn = load_predict_fn_exported(exported_model_path)
print('Time to load model {}'.format(time()-start))
start = time()
questions=['ask_doc: g_t M a_t 23 q_t I have had pain in ear with discharge for last 3 weeks and ear drum has a perforration.',
           'ask_doc: g_t M a_t 24 q_t My periods are delayed, what to do?',
           'ask_doc: g_t F a_t 24 q_t My periods are delayed, what to do?',
           'ask_doc: g_t M a_t 50 q_t I have am losing Weight, and have hypertension. please suggest ?',
           'ask_doc: g_t M a_t 23 q_t I have stiffness in my neck and swollen lymphnodes. I also have rashes on my head. can you suggest medicines ?'
]

times=[]
for question in questions:
    start=time()
    answers = answer(question)
    times.append(time()-start)
    print(answers)
print('Average time per predictions{}'.format(sum(times)/len(times)))

