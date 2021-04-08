from flask import Flask, render_template
from threading import Thread

app = Flask('Ultimate Embed Bot')

@app.route('/')
def home():
    return render_template("statpage.html")

@app.route('/helpful-tutorials-channels')
def tutorials():
  return render_template("tutorials.html")

@app.route('/thanks')
def thanks():
  return render_template("thanks.html")

def run():
  app.run(host='0.0.0.0',port=8080)

def bot_server():
    t = Thread(target=run)
    t.start()
