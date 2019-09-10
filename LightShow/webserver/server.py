from flask import Flask, render_template, request
import json

app = Flask(__name__)

def startServer(queue_in):
    global queue
    queue = queue_in
    app.run(host='0.0.0.0', use_reloader=False)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/changeMode", methods=['POST'])
def changeMode():
    request.json.update({'msg':'changeMode'})
    queue.put(request.json)
    return json.dumps({'status':'OK'})

@app.route("/changeEffect", methods=['POST'])
def changeEffect():
    request.json.update({'msg':'changeEffect'})
    queue.put(request.json)
    return json.dumps({'status':'OK'})
