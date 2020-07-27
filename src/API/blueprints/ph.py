from src.API.blueprints.functions import byRecentDay, byRecentWeek, byTimeperiod, byDate, byRecentYear, byRecentMonth
from flask import Blueprint


ph = Blueprint('ph', __name__)

value = "ph_a_float"
type = "ph"


@ph.route('/solapi/ph/recent/day')
def phDay():
    return byRecentDay(value, type)


@ph.route('/solapi/ph/recent/week')
def phWeek():
    return byRecentWeek(value, type)


@ph.route('/solapi/ph/recent/month')
def phMonth():
    return byRecentMonth(value, type)


@ph.route('/solapi/ph/recent/year')
def phYear():
    return byRecentYear(value, type)


@ph.route('/solapi/ph/date')
def phDate():
    return byDate(value, type)


@ph.route('/solapi/ph/timeperiod')
def phTimeperiod():
    return byTimeperiod(value, type)
