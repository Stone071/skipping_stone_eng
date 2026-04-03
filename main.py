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
import calc

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

@app.route("/hip-belt-buckle")
def hip_belt_buckle():
    return render_template("aluminum-hipbelt-buckle.html")

@app.route("/lifetime-investment-calc")
def lifetime_investment_calc_page():
    return render_template("lifetime-investment-calc.html")

@app.route('/calculate', methods=['POST'])
def main_calc():
    return calc.calculate()

@app.route("/audio-bandpass-filter")
def audio_bandpass_filter():
    return render_template("audio-bandpass-filter.html")

# @app.route('/download')
# def main_download():
#     return calc.download_csv()