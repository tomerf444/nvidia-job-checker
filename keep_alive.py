from flask import Flask
from main import check_jobs

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

@app.route('/check-now')
def run_check():
    result = check_jobs()
    return result

def keep_alive():
    app.run(host='0.0.0.0', port=8080)
