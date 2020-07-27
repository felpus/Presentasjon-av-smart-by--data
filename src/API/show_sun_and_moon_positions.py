from datetime import datetime, date, timedelta

import pytz
import requests

from src.API.isJsonKeyPresent import isJsonKeyPresent


# show_sun_and_moon_positions() retrieves the times when the sun and moon rises,
# is at their highest point, and when they set from the API.

# Data retrieval link retrieved from https://api.met.no/

# is_dst checks if daylight saving time is in effect.
def is_dst(timezone_name):
    # timezone gets the name of the current timezone.
    timezone = pytz.timezone(timezone_name)
    # time_now gets the time of the current timezone.
    time_now = pytz.utc.localize(datetime.utcnow())
    return time_now.astimezone(timezone).dst() != timedelta(0)


def show_sun_and_moon_positions():
    # today gets today's date.
    today = str(date.today())
    # tomorrow gets tomorrow's date.
    tomorrow = str(date.today() + timedelta(1))
    # If daylight saving time is in effect the times will be adjusted to this.
    if is_dst("Europe/Oslo"):
        data_retrieval_url_today = "https://api.met.no/weatherapi/sunrise/2.0/.json?lat=58.2490&lon=8.3776&date=" + \
                                   today + "&offset=+02:00"
        data_retrieval_url_tomorrow = "https://api.met.no/weatherapi/sunrise/2.0/.json?lat=58.2490&lon=8.3776&date=" + \
                                      tomorrow + "&offset=+02:00"
    else:
        # data_retrieval_url_today gets today's data.
        data_retrieval_url_today = "https://api.met.no/weatherapi/sunrise/2.0/.json?lat=58.2490&lon=8.3776&date=" + \
                                   today + "&offset=+01:00"
        # data_retrieval_url_tomorrow gets tomorrow's data.
        data_retrieval_url_tomorrow = "https://api.met.no/weatherapi/sunrise/2.0/.json?lat=58.2490&lon=8.3776&date=" + \
                                      tomorrow + "&offset=+01:00"

    data_today = requests.get(data_retrieval_url_today).json()
    data_tomorrow = requests.get(data_retrieval_url_tomorrow).json()

    # Both sun_and_moon_data_today and sun_and_moon_data_tomorrow get's the specific
    # timestamp for when the sun and moon rises, is at their highest, and sets.
    # sun_and_moon_data_today gets today's timestamp, while sun_and_moon_data_tomorrow gets
    # tomorrow's timestamp.
    sun_and_moon_data_today = data_today["location"]["time"][0]
    sun_and_moon_data_tomorrow = data_tomorrow["location"]["time"][0]

    # This checks if the sun data is available.
    # If the data is available, it will be displayed.
    # If the data is not available, "data missing" will be printed.
    if isJsonKeyPresent(sun_and_moon_data_today, "sunrise"):
        sun_rise = sun_and_moon_data_today["sunrise"]["time"]
    else:
        sun_rise = "Data missing"
    if isJsonKeyPresent(sun_and_moon_data_today, "solarnoon"):
        solar_noon = sun_and_moon_data_today["solarnoon"]["time"]
    else:
        solar_noon = "Data missing"
    if isJsonKeyPresent(sun_and_moon_data_today, "sunset"):
        sun_set = sun_and_moon_data_today["sunset"]["time"]
    else:
        sun_set = "Data missing"

    # This checks if the moon data is available.
    # If the data is available, it will be displayed.
    # If the data is not available, "data missing" will be printed.
    if isJsonKeyPresent(sun_and_moon_data_today, "moonrise"):
        moon_rise = sun_and_moon_data_today["moonrise"]["time"]
    else:
        moon_rise = "Data missing"
    if isJsonKeyPresent(sun_and_moon_data_today, "high_moon"):
        high_moon = sun_and_moon_data_today["high_moon"]["time"]
    else:
        high_moon = "Data missing"
    if isJsonKeyPresent(sun_and_moon_data_today, "moonset"):
        moon_set = sun_and_moon_data_today["moonset"]["time"]
    # In case there is no data for "moonset" for the current day,
    # it checks if there is available data for the next day.
    elif "moonset" not in sun_and_moon_data_today:
        moon_set = sun_and_moon_data_tomorrow["moonset"]["time"]
    else:
        moon_set = "Data missing"

    moon_rise = str(moon_rise)[11:-9]
    high_moon = str(high_moon)[11:-9]
    moon_set = str(moon_set)[11:-9]

    sun_rise = str(sun_rise)[11:-9]
    solar_noon = str(solar_noon)[11:-9]
    sun_set = str(sun_set)[11:-9]

    return sun_rise, solar_noon, sun_set, moon_rise, high_moon, moon_set, today, tomorrow
