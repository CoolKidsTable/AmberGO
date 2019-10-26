from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/',methods = ["GET","POST"])
def index():
    if request.method == "GET":    
        return render_template("input.html")
    elif request.method == "POST":
        return render_template("input2.html",name=request.form["tempusername"])
if __name__ == "__main__":
    app.run()
