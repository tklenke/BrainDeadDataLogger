# app.py or app/__init__.py
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('config')

# Now we can access the configuration variables via app.config["VAR_NAME"].
app.config["DEBUG"]

@app.route("/")
def home():
    return render_template('home.html')

if __name__ == "__main__":
   app.run(host='0.0.0.0')
