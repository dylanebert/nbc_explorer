from flask import Flask, request, render_template
from flask_cors import CORS
import explorer
import crowdsource
import json
import action_sampling

app = Flask(__name__)
CORS(app)

#---explorer---
@app.route('/')
def viewer():
    return render_template('legacy_phrase_viewer.html')

@app.route('/get_legacy_phrases')
def get_legacy_phrases():
    return explorer.get_legacy_phrases()

@app.route('/get_phrase')
def get_phrase_data():
    idx = int(request.args.get('idx'))
    method = request.args.get('method')
    return explorer.get_phrase_data(idx, method)

@app.route('/get_questions')
def get_questions():
    idx = int(request.args.get('idx'))
    return explorer.get_questions(idx)

#---crowdsourcing---
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

#---sequence viewer---
@app.route('/sequence')
def sequence_viewer():
    return render_template('sequence_viewer.html')

#---advanced viewer---
@app.route('/advanced')
def advanced_page():
    return render_template('advanced_viewer.html')

@app.route('/z_dict')
def get_z_dict():
    with open('static/1_1a_task1.json') as f:
        z_dict = f.read()
    return z_dict

#---action sampling---
@app.route('/actions')
def actions():
    return render_template('action_sampling.html')

@app.route('/actions_meta')
def actions_meta():
    return action_sampling.get_paths()

@app.route('/states')
def get_states():
    path = request.args.get('path')
    return action_sampling.get_actions(path)

@app.route('/sample_action')
def sample_action():
    path = request.args.get('path')
    action = int(request.args.get('action'))
    return action_sampling.sample_action(path, action)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
