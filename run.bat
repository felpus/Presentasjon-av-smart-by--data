::==============================================================================================================
:: This file opens the pipenv and runs the getdata script with the raw arg, meant for use by task scheduler.
:: First part needs to show the path to your venv, second part to the Smartcity-Portal folder.
:: Example setup below.
::==============================================================================================================

@echo off
cd /d C:\Users\filip\.virtualenvs\smartcity-portal-BG8kviAX\Scripts & activate & cd /d    C:\Users\filip\Smartcity-Portal & py -m src.Backend.getdata raw