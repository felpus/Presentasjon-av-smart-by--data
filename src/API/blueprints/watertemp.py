from src.API.blueprints.functions import byRecentDay, byRecentWeek, byTimeperiod, byDate, byRecentYear, byRecentMonth
from flask import Blueprint

watertemp = Blueprint('watertemp', __name__)

value = "temperature_b"
type = "watertemp"


@watertemp.route('/solapi/watertemp/recent/day')
def waterTempDay():
    return byRecentDay(value, type)


@watertemp.route('/solapi/watertemp/recent/week')
def waterTempWeek():
    return byRecentWeek(value, type)


@watertemp.route('/solapi/watertemp/recent/month')
def waterTempMonth():
    return byRecentMonth(value, type)


@watertemp.route('/solapi/watertemp/recent/year')
def waterTempYear():
    return byRecentYear(value, type)


@watertemp.route('/solapi/watertemp/date')
def waterTempDate():
    return byDate(value, type)


@watertemp.route('/solapi/watertemp/timeperiod')
def waterTempTimeperiod():
    return byTimeperiod(value, type)
