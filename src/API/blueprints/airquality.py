from src.API.blueprints.functions import byRecentDay, byRecentWeek, byTimeperiod, byDate, byRecentYear, byRecentMonth
from flask import Blueprint


airquality = Blueprint('airquality', __name__)

value = "airquality"
type = "airquality"


@airquality.route('/solapi/airquality/recent/day')
def airQualityDay():
    return byRecentDay(value, type)


@airquality.route('/solapi/airquality/recent/week')
def airQualityWeek():
    return byRecentWeek(value, type)


@airquality.route('/solapi/airquality/recent/month')
def airQualityMonth():
    return byRecentMonth(value, type)


@airquality.route('/solapi/airquality/recent/year')
def airQualityYear():
    return byRecentYear(value, type)


@airquality.route('/solapi/airquality/date')
def airQualityDate():
    return byDate(value, type)


@airquality.route('/solapi/airquality/timeperiod')
def airQualityTimeperiod():
    return byTimeperiod(value, type)
