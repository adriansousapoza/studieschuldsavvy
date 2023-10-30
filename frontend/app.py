from flask import Flask, render_template, request
import sys
from pathlib import Path

parent_dir = Path(__file__).parents[1].absolute()
sys.path.append(str(parent_dir))

from backend.studieschuld import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def form():
    return render_template('input_form.html')

@app.route('/display', methods=['POST'])
def display():
    debt_bsc = request.form['debt_bsc']

    return render_template('display.html', debt_bsc=debt_bsc)

if __name__ == '__main__':
    app.run(debug=True)