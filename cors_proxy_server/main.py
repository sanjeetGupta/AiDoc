import requests
from flask import request,Flask,jsonify
from flask_cors import CORS,cross_origin
import json

app= Flask(__name__)
cors =CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
url = '' ## Kubernetes (Load balancer service) url here
doc_app_endpoint = '/aidoc'

@app.route('/')
@cross_origin()
def hello():
    return('Hello, DOC APP!')


@app.route('/doc_app/',methods=['POST'])
@cross_origin()
def doc_app():
    if request.method == 'POST':
        data = request.get_json()
        print('Received doc_app request: {}'.format(data),flush=True)
        out = requests.post(url+doc_app_endpoint,json=data)
        print(out.json())
        print('tf serving finished processing')
        return json.dumps(out.json())


if __name__ == "__main__":
    print('starting proxy')
    app.run(host = '0.0.0.0',port = 9236)
    
