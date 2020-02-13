from flask import Flask, request, render_template
from flask_cors import CORS
import explorer
import crowdsource
import json

app = Flask(__name__)
CORS(app)

#---explorer---
@app.route('/viewer')
def index():
    return render_template('index.html')

@app.route('/')
def viewer():
    return render_template('phrase_viewer.html')

@app.route('/get_phrases')
def get_phrases():
    return explorer.get_phrases()

@app.route('/get_phrases_old')
def get_phrases_old():
    return explorer.get_phrases_old()

@app.route('/get_phrase')
def get_phrase_data():
    idx = int(request.args.get('idx'))
    method = request.args.get('method')
    return explorer.get_phrase_data(idx, method)

@app.route('/get_questions')
def get_questions():
    idx = int(request.args.get('idx'))
    return explorer.get_questions(idx)

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
    res = json.loads(request.args.get('res'))
    crowdsource.save_response(id, res)
    return 'done'

#---advanced viewer---
@app.route('/advanced')
def advanced_page():
    return render_template('advanced_viewer.html')

@app.route('/z_dict')
def get_z_dict():
    with open('static/1_1a_task1.json') as f:
        z_dict = f.read()
    return z_dict

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
