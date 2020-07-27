# This file is for when you wish to create a new template for a sensor with a specific datatype.
# Fixme all TEMPLATE and replace with the name of your new blueprint.
# Fixme all templateDataTypeName and replace with the name of your new datatype.
# Fixme set value in line 14 to the specific variable you want to get data from in the database.

"""
from src.API.blueprints.functions import byRecentDay, byRecentWeek, byTimeperiod, byDate, byRecentYear, byRecentMonth
from flask import Blueprint


TEMPLATE = Blueprint('TEMPLATE', __name__)

value = "temperature_b"
type = "TEMPLATE"


@TEMPLATE.route('/solapi/TEMPLATE/recent/day')
def templateDataTypeNameDay():
    return byRecentDay(value, type)


@TEMPLATE.route('/solapi/TEMPLATE/recent/week')
def templateDataTypeNameWeek():
    return byRecentWeek(value, type)


@TEMPLATE.route('/solapi/TEMPLATE/recent/month')
def templateDataTypeNameMonth():
    return byRecentMonth(value, type)


@TEMPLATE.route('/solapi/TEMPLATE/recent/year')
def templateDataTypeNameYear():
    return byRecentYear(value, type)


@TEMPLATE.route('/solapi/TEMPLATE/date')
def templateDataTypeNameDate():
    return byDate(value, type)


@TEMPLATE.route('/solapi/TEMPLATE/timeperiod')
def templateDataTypeNameTimeperiod():
    return byTimeperiod(value, type)

"""
