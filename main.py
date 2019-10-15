from flask import Flask, request, render_template
from flask_cors import CORS
import explorer

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crowdsource')
def crowdsource():
    return render_template('crowdsource.html')

@app.route('/get_phrases')
def get_phrases():
    return explorer.get_phrases()

@app.route('/get_phrase')
def get_phrase():
    idx = int(request.args.get('idx'))
    return explorer.get_phrase(idx)

@app.route('/get_svo')
def get_svo():
    idx = int(request.args.get('idx'))
    return explorer.get_svo(idx)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
