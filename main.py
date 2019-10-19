from flask import Flask, request, render_template
from flask_cors import CORS
import explorer
import crowdsource
import json

app = Flask(__name__)
CORS(app)

#---explorer---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_phrases')
def get_phrases():
    phrases = explorer.get_phrases()
    res = {'phrases': phrases, 'k': len(phrases)}
    return json.dumps(res)

@app.route('/get_phrase')
def get_phrase():
    idx = int(request.args.get('idx'))
    return explorer.get_phrase(idx)

@app.route('/get_svo')
def get_svo():
    idx = int(request.args.get('idx'))
    return explorer.get_svo(idx)

#---crowdsource---
@app.route('/crowdsource')
def crowdsource_page():
    return render_template('crowdsource.html')

@app.route('/find_id')
def find_id():
    id = crowdsource.find_id()
    return json.dumps(id)

@app.route('/get_entity')
def get_response():
    id = int(request.args.get('id'))
    entity = crowdsource.get_entity(id)
    return json.dumps(entity)

@app.route('/save_response')
def save_response():
    id = int(request.args.get('id'))
    res = int(request.args.get('res'))
    crowdsource.save_response(id, res)
    return 'done'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
