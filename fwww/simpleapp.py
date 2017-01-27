# app.py or app/__init__.py
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

# Now we can access the configuration variables via app.config["VAR_NAME"].
app.config["DEBUG"]

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
