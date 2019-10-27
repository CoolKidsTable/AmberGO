from flask import Flask, redirect, render_template, request, url_for
from amberScrape import getCenterCoordinates, getSearchRadius, getVehicleImage

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
        try:
            year = int(request.form["model_year"])
        except ValueError:
            year = 2012
        coords = getCenterCoordinates(request.form["street"],request.form["city"],request.form["state"])
        latitude = coords[0]
        longitude = coords[1]
        searchRadius = getSearchRadius(request.form["make"],request.form["model"],year)
        carImagesrc = getVehicleImage(request.form["make"],request.form["model"],year)
        return render_template("gasLocMap.html", centerLatitude=latitude, centerLongitude=longitude, searchRadius=searchRadius, carImagesrc=carImagesrc, street=request.form["street"], city=request.form["city"], state=request.form["state"], make=request.form["make"], model=request.form["model"], model_year=request.form["model_year"], licence_plate=request.form["licence_plate"], color=request.form["color"])

if __name__ == "__main__":
    app.run()
