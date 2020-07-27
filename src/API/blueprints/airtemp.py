from src.API.blueprints.functions import byRecentDay, byRecentWeek, byTimeperiod, byDate, byRecentYear, byRecentMonth
from flask import Blueprint


airtemp = Blueprint('airtemp', __name__)

value = "temperature_float"
type = "airtemp"


@airtemp.route('/solapi/airtemp/recent/day')
def airTempDay():
    return byRecentDay(value, type)


@airtemp.route('/solapi/airtemp/recent/week')
def airTempWeek():
    return byRecentWeek(value, type)


@airtemp.route('/solapi/airtemp/recent/month')
def airTempMonth():
    return byRecentMonth(value, type)


@airtemp.route('/solapi/airtemp/recent/year')
def airTempYear():
    return byRecentYear(value, type)


@airtemp.route('/solapi/airtemp/date')
def airTempDate():
    return byDate(value, type)


@airtemp.route('/solapi/airtemp/timeperiod')
def airTempTimeperiod():
    return byTimeperiod(value, type)
