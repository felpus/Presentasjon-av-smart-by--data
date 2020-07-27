import os
import sys
import threading
import time
from datetime import datetime
from time import sleep

import requests
from func_timeout import FunctionTimedOut, func_timeout

import src.config as config
from src.API.formatVariable import formatVariable
from src.API.isJsonKeyPresent import isJsonKeyPresent
from src.Backend import insertdata
from src.Backend.insertdata import returnSensorIds

# https://docs.telenorconnexion.com/mic/rest-api/
# Url variables

loginUrl = "https://3ohe8pnzfb.execute-api.eu-west-1.amazonaws.com/prod/auth/login"
refreshUrl = "https://3ohe8pnzfb.execute-api.eu-west-1.amazonaws.com/prod/auth/refresh"
findUrl = "https://3ohe8pnzfb.execute-api.eu-west-1.amazonaws.com/prod/things/find"
thingTypesUrl = "https://3ohe8pnzfb.execute-api.eu-west-1.amazonaws.com/prod/thingtypes"
resourcesUrl = "https://3ohe8pnzfb.execute-api.eu-west-1.amazonaws.com/prod/resources"

# Dict that contains a "hashmap" for thingType labels. key is thingType id.
thingsDict = {}


def clear():
    os.system('cls')


# Function that looks up all resources for all thingTypes for the connected account.
def getResources():
    try:
        global resourcesList
        global resourcesListWithType
        r = requests.get(resourcesUrl, headers={"x-api-key": config.apikey, "Authorization": config.authtoken})
        data = r.json()
        if data == {'message': 'The incoming token has expired'}:
            print(data)
            print("Refreshing token...")
            renewToken()
            getResources()
        else:
            # Creates two lists of resources that exists for all things connected to account
            # resourcesList contains the names of the resources.
            resourcesList = []
            # resourcesListWithType contains name and the type of data.
            resourcesListWithType = []
            for item in data:
                for item in data[item]["resources"]:
                    checkIfExists = item["name"]
                    checkIfExistsLowerCase = checkIfExists.lower()
                    if checkIfExistsLowerCase not in resourcesList:
                        resourcesList.append(checkIfExistsLowerCase)
                        resourcesListWithType.append([checkIfExistsLowerCase, item["type"]])
            # print(resourcesList)
            # print(resourcesListWithType)
            return resourcesList, resourcesListWithType
    except Exception as E:
        print("getResources error: ", E)


# Function that looks up resources for a specific thingType - DEPRECATED
def getResourcesForSensorType(thingTypeId):
    try:
        resourcesUrlId = "https://3ohe8pnzfb.execute-api.eu-west-1.amazonaws.com/prod/resources/" + thingTypeId
        r = requests.get(resourcesUrlId, headers={"x-api-key": config.apikey, "Authorization": config.authtoken})
        data = r.json()
        if data == {'message': 'The incoming token has expired'}:
            print(data)
            print("Refreshing token...")
            renewToken()
            getResourcesForSensorType(thingTypeId)
        else:
            resources = data["resources"]
            for item in resources:
                itemName = item["name"]
                itemNameLowercase = itemName.lower()
                resources.append([itemNameLowercase, item["type"]])
            # print(resources)
            return resources

    except Exception as E:
        print("getResourcesForSensorType error: ", E)


# Creates all sensor tables
def createAllSensorTables():
    try:
        sensorList = returnSensorIds()
        for item in sensorList:
            id = item["id"]
            url = "https://3ohe8pnzfb.execute-api.eu-west-1.amazonaws.com/prod/things?thingName=" + id
            createSensorTable(url)
    except Exception as E:
        print("createAllSensorTables error: ", E)


# Used by createAllSensorTables to create a table
def createSensorTable(url):
    try:
        r = requests.get(url, headers={"x-api-key": config.apikey, "Authorization": config.authtoken})
        data = r.json()
        if data == {'message': 'The incoming token has expired'}:
            print(data)
            print("Refreshing token...")
            renewToken()
            createSensorTable(url)
        elif isJsonKeyPresent(data, "message"):
            print(data["message"]["messageKey"],
                  "The thing you are looking for from " + url + " might not be available on this Telenorconnexion "
                                                                "account.")
            return
        else:
            thingLabel = data["label"]
            thingLabel = formatVariable(thingLabel)
            thingType = data["thingType"]
            thingName = data["thingName"]
            reported = data["shadow"]["state"]["reported"]
            thingsDict[thingName] = thingLabel

            # print(reported)
            for item in list(reported):
                item2 = item.lower()
                reported[item2] = reported.pop(item)
            foundList = []
            # print(reported)
            # print(resourcesList)
            # print(resourcesListWithType)
            for item in resourcesListWithType:
                resource = item[0]
                # Checks if item in reported exists in resourcesList.
                if isJsonKeyPresent(reported, resource):
                    if resource not in foundList:
                        foundList.append(item)

            # print(foundList)

            sensorResourcesList = []
            sensorResourcesList.append(thingName)
            sensorResourcesList.append(thingType)

            for item in foundList:
                sensorResourcesList.append(item)

            # print(sensorResourcesList)

            query = insertdata.createQuery(foundList, thingLabel)

            # print(query)

            insertdata.insertSensorTable(query, thingLabel, thingName)

    except Exception as E:
        print("createSensorTable thingName: " + thingName + " error: ", E)
        print(
            "Information: If an error is for example 'shadow', it means that a 'thing' does not have the json content "
            "we are looking for. Fix this by making sure the thing has a 'resource' to return!")


# Returns data from the thing specified in the URL variable, used by getDataFromThings
def getData(url):
    try:
        r = requests.get(url, headers={"x-api-key": config.apikey, "Authorization": config.authtoken})
        data = r.json()
        if data == {'message': 'The incoming token has expired'}:
            print(data)
            print("Refreshing token...")
            renewToken()
            return getData(url)
        else:
            thingType = data["thingType"]
            thingName = data["thingName"]
            reported = data["shadow"]["state"]["reported"]
            # print(reported)
            for item in list(reported):
                item2 = item.lower()
                reported[item2] = reported.pop(item)
            foundList = []
            # print(reported)
            # print(resourcesList)
            # print(resourcesListWithType)
            for item in resourcesList:
                # Checks if item in reported exists in resourcesList.
                if isJsonKeyPresent(reported, item):
                    if item not in foundList:
                        foundList.append(item)

            # print(foundList)
            returningList = []
            returningList.append(thingName)
            returningList.append(thingType)

            for item in foundList:
                returningList.append([item, reported[item]])

            # Will return an error if a "thing" does not have the json content we are looking for. E.g "shadow".
            # print(returningList)
            return returningList

    except Exception as E:
        print("getData thingName: " + thingName + " error: ", E)
        print(
            "Information: If an error is for example 'shadow', it means that a 'thing' does not have the json content "
            "we are looking for. Fix this by making sure the thing has a 'resource' to return!")


# Inserts all reported data from all things connected to the account into a database.
def getDataFromThings():
    try:
        idList = returnSensorIds()
        print("Getting data at", datetime.now())
        for item in idList:
            now1 = datetime.now()
            now2 = now1.strftime("%Y/%m/%d %H:%M:%S")
            dateTime = now2
            # print(dateTime)
            id = item["id"]
            url = "https://3ohe8pnzfb.execute-api.eu-west-1.amazonaws.com/prod/things?thingName=" + id
            # print(url)
            try:
                returnedList = getData(url)
                # print(returnedList)
                thingName = returnedList[0]
                returnedList.pop(0)
                thingTypeId = returnedList[0]
                returnedList.pop(0)
                insertdata.insertSensorData(thingName, thingTypeId, returnedList, thingsDict, dateTime)
            except Exception as e:
                print(e)
                print("Error in try bloc at getDataFromThings(). URL: " + url)
                pass
    except Exception as E:
        print("getDataFromThings error: ", E)


# Updates tokens by the use of user credentials.
def getTokens(u, p):
    try:
        r = requests.post(loginUrl, headers={"x-api-key": config.apikey, "Content-Type": "application/json"},
                          json={"userName": u, "password": p})
        data = r.json()
        config.authtoken = (data["credentials"]["token"])
        config.refreshtoken = (data["credentials"]["refreshToken"])
        clear()
        print("Credentials accepted, tokens updated.")
        print("You can also start the program with the arg """"printtokens"""" to see your auth/refresh tokens,"
              " this lets you easily copy your tokens to config.py")
    except Exception as E:
        print("getTokens error: ", E, data["message"]["message"])
        sys.exit()


# Prints tokens by the use of user credentials.
def printTokens(u, p):
    try:
        if config.apikey == "":
            print("Missing x-api-key. To get the API key, please contact your Telenor Connexion representative.")
            sys.exit()
        else:
            r = requests.post(loginUrl, headers={"x-api-key": config.apikey, "Content-Type": "application/json"},
                              json={"userName": u, "password": p})
            data = r.json()
            print("")
            print("Authorisation token: " + data["credentials"]["token"])
            print("")
            print("Refresh token: " + data["credentials"]["refreshToken"])
            print("")
            print(
                "These tokens can be placed into config.py to avoid entering a username and password every time"
                " you start the program.")
            sys.exit()
    except Exception as E:
        print("printTokens error: ", E, data["message"]["message"])
        sys.exit()


# Renews authorisation token.
def renewToken():
    try:
        r = requests.post(refreshUrl, headers={"x-api-key": config.apikey, "Content-Type": "application/json"},
                          json={"refreshToken": config.refreshtoken})
        data = r.json()
        config.authtoken = (data["credentials"]["token"])
        print("Token refreshed.")
    except Exception as E:
        print("renewToken error: ", E)


# Finds all sensor types connected to the account and inserts them into the thingType table.
def getSensorTypes():
    try:
        r = requests.get(thingTypesUrl, headers={"x-api-key": config.apikey, "Authorization": config.authtoken})
        data = r.json()
        if data == {'message': 'The incoming token has expired'}:
            print(data)
            print("Refreshing token...")
            renewToken()
            getSensorTypes()
        else:
            for item in data:
                # print(data)
                thingTypeId = item["id"]
                # existingResources = getResourcesForType(id)
                # print(existingResourcesForThingType)
                label = item["label"]
                description = item["description"]
                # print(resourcesListWithType)
                label = formatVariable(label)
                # print(existingResources)

                # Creates a query for the function below. - DEPRECATED
                # query = insertdata.createQuery(existingResources, label)
                # Creates a table for the thingType - DEPRECATED
                # insertdata.createThingTypeTable(query, label, id)

                # Adds sensor types to a thingTypes table in the database.
                insertdata.addSensorTypes(thingTypeId, label, description)

                # print("thingTypeId:", item["id"], end=", "), print("thingTypeLabel:", item["label"])
    except Exception as E:
        print("getSensorTypes error: ", E)


# Finds all things connected to the account and places them into a table.
def getSensors():
    try:
        r = requests.post(findUrl, headers={"x-api-key": config.apikey, "Authorization": config.authtoken}, json={
            "query": {"size": 10000, "query": {"match_all": {}}}})
        data = r.json()
        if data == {'message': 'The incoming token has expired'}:
            print(data)
            print("Refreshing token...")
            renewToken()
            getSensors()
        else:
            # Checks the elastisearch for sensors.
            data2 = (data["hits"]["hits"])
            for i in data2:
                item = i["_source"]
                # print(item)
                if item.get("state") is not None:
                    latlngCheck = item["state"]
                    if isJsonKeyPresent(latlngCheck, "latlng"):
                        latlng = item["state"]["latlng"]
                        id = item["thingName"]
                        label = item["label"]
                        if item.get("description") is not None:
                            description = item["description"]
                        else:
                            description = ""
                        thingType = item["thingType"]
                        label = formatVariable(label)
                        insertdata.addSensors(id, label, description, thingType, latlng)
                    else:
                        latlng = ""
                        id = item["thingName"]
                        label = item["label"]
                        if item.get("description") is not None:
                            description = item["description"]
                        else:
                            description = ""
                        thingType = item["thingType"]
                        label = formatVariable(label)
                        insertdata.addSensors(id, label, description, thingType, latlng)
                else:
                    latlng = ""
                    id = item["thingName"]
                    label = item["label"]
                    if item.get("description") is not None:
                        description = item["description"]
                    else:
                        description = ""
                    thingType = item["thingType"]
                    label = formatVariable(label)
                    insertdata.addSensors(id, label, description, thingType, latlng)
    except Exception as E:
        print("getSensors error: ", E)


# Creates tables for sensors and runs getDataFromThings once.
def raw():
    renewToken()
    getResources()
    getSensorTypes()
    getSensors()
    createAllSensorTables()
    getDataFromThings()


# Updates database with new sensors if they exist.
def init():
    getResources()
    getSensorTypes()
    getSensors()
    createAllSensorTables()


# Updates database with new sensors if they exist, also initiates the getDataFromThings loop.
def run():
    global programStarted
    programStarted = time.time()
    global retrieve
    retrieve = True

    getResources()
    getSensorTypes()
    getSensors()
    createAllSensorTables()

    threadRetrieval = threading.Thread(target=loop, daemon=True)
    threadRetrieval.start()

    while True:
        i = input()
        if i.lower() == "updatedatabase":
            print("Updating database...")
            init()
        elif i.lower() == "updatesensors":
            print("Forcing sensordata update...")
            getDataFromThings()
        elif i.lower() == "time":

            print("Script was started at:", datetime.fromtimestamp(programStarted))
            try:
                if starttime:
                    print("Last restart of loop:", datetime.fromtimestamp(starttime))
                    print("Remaining time before next update: ",
                          (config.sleepinterval - ((time.time() - starttime) % config.sleepinterval)))
                else:
                    print("Data retrieval process not yet started.")
            except Exception:
                pass
            print("Current interval:", config.sleepinterval)
        elif i.lower() == "changeinterval":
            print("Enter new interval:")
            interval = input()
            try:
                if interval == "":
                    print("Invalid input, must be a number.")
                    continue
                interval = int(interval)
            except Exception:
                print("Invalid input, must be a number.")
                continue
            if isinstance(interval, int):
                print("Old interval:", config.sleepinterval)
                config.sleepinterval = interval
                print("New interval:", config.sleepinterval)
        elif i.lower() == "pause":
            if not retrieve:
                print("Data retrieval is already paused, type resume to resume data retrieval.")
            else:
                print("Pausing data retrieval...")
                retrieve = False
        elif i.lower() == "resume":
            if retrieve:
                print("Data retrieval is ongoing, type pause to pause data retrieval.")
            else:
                print("Resuming data retrieval...")
                retrieve = True
        elif i.lower() == "stop":
            print("Stopping...")
            sys.exit()
        elif i.lower() == "threads":
            print(threading.activeCount())
        elif i.lower() == "help":
            print(
                "Valid commands are: updatedatabase, updatesensors, time, changeinterval, pause, resume, stop, and "
                "threads.")
        else:
            continue


# Runs getDataFromThings on an interval based on config.sleepinterval.
def loop():
    if config.waitforsync:
        # Syncs clock with minute specified.
        print("Waiting for sync...")
        while datetime.now().minute not in {0, 15, 30, 45}:
            sleep(1)

    global starttime
    starttime = time.time()

    def do():
        getDataFromThings()

    # Restarts every 100th time.
    for _ in range(100):
        if retrieve:
            try:
                # Times out if do() uses more than 5 minutes.
                func_timeout(300, do)
            except FunctionTimedOut:
                print("getDataFromThings() in do() could not complete within 5 minutes and was terminated.")
                break
        else:
            print("Data retrieval is paused, next interval in",
                  config.sleepinterval - ((time.time() - starttime) % config.sleepinterval), "seconds")

        # Maintains system clock sync and the sleep timer.
        time.sleep(config.sleepinterval - ((time.time() - starttime) % config.sleepinterval))

    loop()


# Starts either run() or raw() based on args.
def start():
    for a in sys.argv:
        if a == "altlogin":
            u = input("Enter your Telenorconnexion username:")
            p = input("Enter your Telenorconnexion password:")
            getTokens(u, p)
        elif a == "printtokens":
            u = input("Enter your Telenorconnexion username:")
            p = input("Enter your Telenorconnexion password:")
            printTokens(u, p)
        elif a == "raw":
            if config.apikey == "":
                print("Missing API key, script cannot run with the raw arg without a complete config file.")
                sys.exit()
            if config.authtoken == "":
                print("Missing authtoken, script cannot run with the raw arg without a complete config file.")
                sys.exit()
            if config.refreshtoken == "":
                print("Missing API key, script cannot run with the raw arg without a complete config file.")
                sys.exit()
            raw()
            sys.exit()
    if config.apikey == "":
        print("Missing API key. Add one in config.py or enter your key:")
        config.apikey = input()
    if config.authtoken == "":
        print("Missing authtoken. Add an authtoken token in config.py or enter your credentials:")
        u = input("Enter your Telenorconnexion username:")
        p = input("Enter your Telenorconnexion password:")
        getTokens(u, p)
    run()


if __name__ == "__main__":
    start()
