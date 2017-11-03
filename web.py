from config import * 
from commands import *

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/" + ADMIN_PASSWORD, methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        # If it's a get, display the huy
        return render_template("home.html", templates=load_commands(), error="")
    if request.method == 'POST':
        if 'key' not in request.form:
            return "No Key!", 400
        if 'value' not in request.form:
            return "No Value!", 400

        key = request.form['key']
        value = request.form['value']

        templates = load_commands()
        templates[key] = value
        save_commands(templates)

        return render_template("home.html", templates=load_commands(), error="")
