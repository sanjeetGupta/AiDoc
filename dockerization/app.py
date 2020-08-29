from flask import Flask, request
import json
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import tensorflow_text
from time import time

app = Flask(__name__)


def answer(questions):
    return [ans.decode('utf-8') for ans in predict_fn(questions)]

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

#############################################
exported_model_path = 'model/3'
print('loading model')
predict_fn = load_predict_fn_exported(exported_model_path)
print('loaded model')
###########################################


@app.route('/')
def hello():
    return('Hello, AI DOC')


@app.route("/aidoc",methods=['POST'])
def process_request():
    try:
        error_msg = 'error while loading model'
        start = time()
        error_msg = 'error while reading request'
        input_json = request.get_json()
        error_msg = 'error while running inference'
        print(input_json)
        questions = input_json['inputs']
        print(questions,flush = True)
        answers =  answer(questions)
        print('Total Time for inference: {}'.format(time() - start))
        answer_dt = parse_answer(answers[0])
        print('Total Time taken: {}'.format(time()- start))
        print(answer_dt, flush=True)
        return json.dumps({"message":"success!","result":answer_dt})
    except Exception as e:
        print('Error:' + error_msg,flush = True)
        return json.dumps({"message":"Error: "+error_msg, "Exception":repr(e)}),500

def parse_answer(answer):
    dt = {}
    splits = answer.split('cat_t')
    answer = splits[1].strip()
    splits = answer.split('spc_t')
    dt['cat'] =  splits[0].strip()
    answer = splits[1].strip()
    splits = answer.split('sym_t')
    dt['spec'] =  splits[0].strip()
    answer = splits[1].strip()
    splits = answer.split('ans_t')
    dt['sym'] =  splits[0].strip()
    dt['answer'] = splits[1].strip()
    return dt



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8501,threaded = False)
