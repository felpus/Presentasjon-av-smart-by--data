import pymysql
from flask import jsonify
from flask import request

from src.config import mysql


def byRecentDay(value, type):
    try:
        query_parameters = request.args
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        sensorid = query_parameters.get('sensorid')

        findtable = "SELECT label FROM sensors where id = %s;"
        cursor.execute(findtable, sensorid)
        table = cursor.fetchone()
        table = table["label"]
        cursor.execute(
            "SELECT ROUND(AVG(" + value + "), 1) as " + type + ", min(" + value + ") as min, max(" + value + ") as max, HOUR(datetime) as hour, datetime FROM " + table + " WHERE DATE_SUB(datetime, INTERVAL 1 HOUR) And datetime > DATE_SUB(NOW(), INTERVAL 1 DAY) GROUP BY hour(datetime);")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def byRecentWeek(value, type):
    try:
        query_parameters = request.args
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        sensorid = query_parameters.get('sensorid')

        findtable = "SELECT label FROM sensors where id = %s;"
        cursor.execute(findtable, sensorid)
        table = cursor.fetchone()
        table = table["label"]
        cursor.execute(
            "SELECT ROUND(AVG(" + value + "), 1) as " + type + ", min(" + value + ") as min, max(" + value + ") as max, datetime FROM " + table + " WHERE DATE_SUB(datetime, INTERVAL 1 DAY) And datetime > DATE_SUB(NOW(), INTERVAL 1 WEEK) GROUP BY date(datetime), hour(datetime);")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def byRecentMonth(value, type):
    try:
        query_parameters = request.args
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        sensorid = query_parameters.get('sensorid')

        findtable = "SELECT label FROM sensors where id = %s;"
        cursor.execute(findtable, sensorid)
        table = cursor.fetchone()
        table = table["label"]
        cursor.execute(
            "SELECT ROUND(AVG(" + value + "), 1) as " + type + ", min(" + value + ") as min, max(" + value + ") as max, date(datetime) as date FROM " + table + " WHERE DATE_SUB(datetime, INTERVAL 1 WEEK) And datetime > DATE_SUB(NOW(), INTERVAL 1 MONTH) GROUP BY day(datetime);")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def byRecentYear(value, type):
    try:
        query_parameters = request.args
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        sensorid = query_parameters.get('sensorid')

        findtable = "SELECT label FROM sensors where id = %s;"
        cursor.execute(findtable, sensorid)
        table = cursor.fetchone()
        table = table["label"]
        cursor.execute(
            "SELECT ROUND(AVG(" + value + "), 1) as " + type + ", min(" + value + ") as min, max(" + value + ") as max, monthname(datetime) as month, date(datetime) as date FROM " + table + " WHERE DATE_SUB(datetime, INTERVAL 1 WEEK) And datetime > DATE_SUB(NOW(), INTERVAL 13 month) GROUP BY year(datetime), month(datetime);")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def byDate(value, type):
    try:
        query_parameters = request.args
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        year = query_parameters.get('year')
        month = query_parameters.get('month')
        day = query_parameters.get('day')
        sensorid = query_parameters.get('sensorid')

        findtable = "SELECT label FROM sensors where id = %s;"
        cursor.execute(findtable, sensorid)
        table = cursor.fetchone()
        table = table["label"]

        to_filter = []

        query = "SELECT ROUND(AVG(" + value + "), 1) as " + type + ", min(" + value + ") as min, max(" + value + ") as max, week(datetime) as week, datetime FROM " + table + " WHERE year(datetime) = %s"

        to_filter.append(year)
        if month:
            query += " AND month(datetime) = %s"
            to_filter.append(month)
            if day:
                query += " AND day(datetime) = %s GROUP BY hour(datetime);"
                to_filter.append(day)
            else:
                query += " GROUP BY day(datetime);"
        else:
            query += " GROUP BY month(datetime);"
        if not (year):
            return not_found(404)

        # print(query)
        cursor.execute(query, to_filter)

        row = cursor.fetchall()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def byTimeperiod(value, type):
    try:
        query_parameters = request.args
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        sensorid = query_parameters.get('sensorid')
        startdate = query_parameters.get('startdate')
        enddate = query_parameters.get('enddate')
        groupby = query_parameters.get('groupby')

        if not (sensorid and startdate and enddate):
            return not_found(404)

        findtable = "SELECT label FROM sensors where id = %s;"
        cursor.execute(findtable, sensorid)
        table = cursor.fetchone()
        table = table["label"]

        to_filter = []

        query = "SELECT ROUND(AVG(" + value + "), 1) as " + type + ", min(" + value + ") as min, max(" + value + ") as max, datetime FROM " + table + " WHERE (datetime BETWEEN %s AND %s) "

        if groupby == "year":
            query += "GROUP BY year(datetime)"
        elif groupby == "month":
            query += "GROUP BY year(datetime), month(datetime)"
        elif groupby == "week":
            query += "GROUP BY year(datetime), month(datetime), week(datetime)"
        elif groupby == "day":
            query += "GROUP BY year(datetime), month(datetime), week(datetime), day(datetime)"
        elif groupby == "hour":
            query += "GROUP BY year(datetime), month(datetime), week(datetime), day(datetime), hour(datetime)"

        query += ";"

        to_filter.append(startdate)
        to_filter.append(enddate)

        # print(query)
        cursor.execute(query, to_filter)

        row = cursor.fetchall()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def not_found(error=None):
    message = {
        'status': 404,
        'Error': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp
