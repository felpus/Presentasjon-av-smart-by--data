from flask import render_template, Blueprint
from src.API.show_sun_and_moon_positions import show_sun_and_moon_positions

ltm = Blueprint('ltm', __name__)


@ltm.route('/')
def index():
    try:
        sun_rise, solar_noon, sun_set, moon_rise, high_moon, moon_set, today, tomorrow = show_sun_and_moon_positions()

        return render_template('webinterface.html', sun_rise=sun_rise, solar_noon=solar_noon, sun_set=sun_set,
                               moon_rise=moon_rise, high_moon=high_moon, moon_set=moon_set, today=today,
                               tomorrow=tomorrow)

    except Exception as E:
        print("index error: ", E)


@ltm.route('/iframe')
def iframe():
    try:
        return render_template('iframechart.html')

    except Exception as E:
        print("index error: ", E)


# vet ikke om dette er den beste  måten å gjøre det på, men fikk det ikke til å fungere ved å referere til en filplassering
@ltm.route('/chartjs')
def chartjs():
    try:
        return render_template('chart.js')

    except Exception as E:
        print("index error: ", E)


@ltm.route('/main')
def main():
    try:
        return render_template('webinterface.js')

    except Exception as E:
        print("index error: ", E)
