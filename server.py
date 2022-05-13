from flask import Flask, request, Response
import jsonpickle
import json
import random
app = Flask(__name__)

def key_gen():
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    key = ""
    i = 0
    for i in range(5):
        for j in range(4):
            key += random.choice(alphabet)
        if i < 4:
            key += "-"
    return key

@app.route('/keygen', methods=['GET'])
def check():
    key = key_gen()
    with open('json_data.json', 'w') as outfile:
        json.dump(key, outfile)
    output = {}
    output['status'] = "Key generated"
    response_pickled = jsonpickle.encode(output)
    return Response(response=response_pickled, status=200, mimetype="application/json")

def run_flask():
    app.run(debug=False, host='127.0.0.1', port=8090)

# print(key_gen())
run_flask()