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
        
@app.route('/starttalking',methods = ["GET","POST"])
def index():
    if request.method == "GET":    
        return render_template("input.html")
    elif request.method == "POST":
        if request.form["selectinput"] == "I need help":
            return redirect(url_for("needhelp"))
        else:
            return redirect(url_for("wanttohelp"))
        return render_template("input2.html",name=request.form["tempusername"])

@app.route('/',methods = ["GET","POST"])
def report():
    if request.method == "GET":    
        return render_template("reportpage.html")
    elif request.method == "POST":
        return render_template("gasLocMap.html", street=request.form["street"],city=request.form["city"],state=request.form["state"],make=request.form["make"],model=request.form["model"],model_year=request.form["model_year"],licence_plate=request.form["licence_plate"],color=request.form["color"])

if __name__ == "__main__":
    app.run()
