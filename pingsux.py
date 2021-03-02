from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "yo chill,bots on"

def run():
  app.run(host='0.0.0.0',port=8080)

def up():
  t = Thread(target=run)
  t.start()