from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

@app.route('/needhelp',methods = ["GET","POST"])
def needhelp():
    if request.method == "GET":
        return render_template("reportpage.html")

@app.route('/wanttohelp',methods = ["GET","POST"])
def wanttohelp():
    if request.method == "GET":
        return render_template("assistpage.html")
        
@app.route('/',methods = ["GET","POST"])
def index():
    if request.method == "GET":    
        return render_template("input.html")
    elif request.method == "POST":
        if request.form["selectinput"] == "I need help":
            return redirect(url_for("needhelp"))
        else:
            return redirect(url_for("wanttohelp"))
        return render_template("input2.html",name=request.form["tempusername"])

if __name__ == "__main__":
    app.run()
