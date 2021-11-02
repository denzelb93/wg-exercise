from flask import Flask
from controllers import GetController

app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/<path:index>', methods=['GET'])
def getObject(index=None):
    return GetController(index)()

app.run(host='0.0.0.0', port=80)


