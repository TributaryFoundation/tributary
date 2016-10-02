from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start')
def start():
    return render_template('start.html')


@app.route('/info', methods=['GET', 'POST'])
def info():
    if request.method == 'POST':
        return repr(request.form)
    return render_template('info.html')


@app.route('/received')
def received():
    return render_template('received.html')


@app.route('/confirmed')
def confirmed():
    return render_template('confirmed.html')
