from flask import Flask

app = Flask(__name__)

@app.route("/defualt/<name>/<days>/<hours>")
def defualt(name, days, hours):
  return 'the value is: ' + name + days + hours

if __name__ == "__main__":
  app.run()