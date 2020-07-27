import pymysql
from flask import Flask, jsonify, request, render_template

from src.API.CustomJSONEncoder import CustomJSONEncoder
from src.API.blueprints.airquality import airquality
from src.API.blueprints.airtemp import airtemp
from src.API.blueprints.longTermMeasurements import ltm
from src.API.blueprints.ph import ph
from src.API.blueprints.watertemp import watertemp
from src.API.blueprints.windspeed import windspeed
from src.config import mysql

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
app.register_blueprint(ltm)
app.register_blueprint(watertemp)
app.register_blueprint(airtemp)
app.register_blueprint(airquality)
app.register_blueprint(windspeed)
app.register_blueprint(ph)


@app.route('/solapi')
def solapi():
    try:
        return render_template("solapi.html")
    except Exception as E:
        print("index error: ", E)


@app.route(
    '/solapi/recent/latest')
def latest():
    try:
        query_parameters = request.args
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        sensorid = query_parameters.get('sensorid')

        findtable = "SELECT label FROM sensors where id = %s;"
        cursor.execute(findtable, sensorid)
        table = cursor.fetchone()
        table = table["label"]

        query = "SELECT * FROM " + table + " order by datetime DESC LIMIT 1;"
        cursor.execute(query)
        rows = cursor.fetchone()
        # print(rows)
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/solapi/rawdata/date')
def rawDataDate():
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

        query = "SELECT * FROM " + table + " WHERE year(datetime) = %s"

        to_filter.append(year)
        if month:
            query += " AND month(datetime) = %s"
            to_filter.append(month)
            if day:
                query += " AND day(datetime) = %s;"
                to_filter.append(day)
        if not (year and sensorid):
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


@app.route('/solapi/sensors')
def getSensors():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM sensors;")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/solapi/rawdata/timeperiod')
def rawDataTimeperiod():
    try:
        query_parameters = request.args
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        sensorid = query_parameters.get('sensorid')
        startdate = query_parameters.get('startdate')
        enddate = query_parameters.get('enddate')

        if not (sensorid and startdate and enddate):
            return not_found(404)

        findtable = "SELECT label FROM sensors where id = %s;"
        cursor.execute(findtable, sensorid)
        table = cursor.fetchone()
        table = table["label"]

        to_filter = []

        query = "SELECT * FROM " + table + " WHERE (datetime BETWEEN %s AND %s);"

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


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'Error': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == '__main__':
    app.run(host="localhost")
