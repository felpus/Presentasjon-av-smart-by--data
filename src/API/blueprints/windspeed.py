from flask import Blueprint

from src.API.blueprints.functions import byRecentDay, byRecentWeek, byTimeperiod, byDate, byRecentYear, byRecentMonth

windspeed = Blueprint('windspeed', __name__)

value = "windspeed"
type = "windspeed"


@windspeed.route('/solapi/windspeed/recent/day')
def windSpeedDay():
    return byRecentDay(value, type)


@windspeed.route('/solapi/windspeed/recent/week')
def windSpeedWeek():
    return byRecentWeek(value, type)


@windspeed.route('/solapi/windspeed/recent/month')
def windSpeedMonth():
    return byRecentMonth(value, type)


@windspeed.route('/solapi/windspeed/recent/year')
def windSpeedYear():
    return byRecentYear(value, type)


@windspeed.route('/solapi/windspeed/date')
def windSpeedDate():
    return byDate(value, type)


@windspeed.route('/solapi/windspeed/timeperiod')
def windSpeedTimeperiod():
    return byTimeperiod(value, type)
