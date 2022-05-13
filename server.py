from flask import Flask, request, Response
import jsonpickle
app = Flask(__name__)

def key_gen():
    pass

@app.route('/check', methods=['GET'])
def check():
    output = {}
    output['status'] = "Service running"
    response_pickled = jsonpickle.encode(output)
    return Response(response=response_pickled, status=200, mimetype="application/json")

def run_flask():
    app.run(debug=False, host='127.0.0.1', port=8090)