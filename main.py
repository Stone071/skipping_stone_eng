######################################################
# main.py
#
# This site will display some personal/engineering 
# projects I've worked on. Python framework provides
# the flexibility to serve python projects live on the
# site.
#
# Zachary Stone, March 2026
######################################################
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/solar-thermal-controller")
def solar_thermal_controller():
    return render_template("solar-thermal-controller.html")

@app.route("/seesaw-island-riddle")
def seesaw_island_riddle():
    return render_template("seesaw-island-riddle.html")

@app.route("/bottle-cap-imager")
def bottle_cap_imager():
    return render_template("bottle-cap-imager.html")