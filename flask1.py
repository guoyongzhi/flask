from flask import Flask, render_template, request
from flask import render_template_string
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")
    # return 'Hello World!'

# @app.route("/index")
# def index():



if __name__ == '__main__':
    app.run(debug=True, port='8080', host='127.0.0.1')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
