# Checks if a json object contains the key variable.
def isJsonKeyPresent(json, key):
    if key in json:
        return True
    else:
        return False
