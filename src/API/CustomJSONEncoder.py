import decimal
from datetime import date

from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                result = obj.strftime("%a, %d %B %Y %H:%M")  # https://docs.python.org/3/library/datetime.html
                return result
            if isinstance(obj, decimal.Decimal):  # Allows the database to return bigint values.
                return int(obj)
            iterable = iter(obj)
        except TypeError as e:
            print(e)
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
