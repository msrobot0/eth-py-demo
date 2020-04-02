from flask import Flask, render_template, request
from intention.intention import Intention
app = Flask(__name__)

@app.route('/')
def echo_intention():
    return render_template('index.html')

@app.route('/intention', methods=['GET', 'POST'])
def make_intention():
    if request.method == 'POST':
        msg = request.form['intention']
        current_intention =Intention(None,None,None,None)
        current_intention.echo_intention(msg)
        return render_template('index.html', intention=current_intention)
    else:
        return render_template('index.html')
