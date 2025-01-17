# imports ===================
from fastapi import APIRouter
#timezone
import os
import time
from datetime import datetime
os.environ['TZ'] = 'America/Sao_Paulo'
time.tzset()

router = APIRouter()

@router.get('/', summary='Welcome info')
def welcome():
    return {
        "server_datetime_gmt-3":datetime.now().strftime("%Y-%m-%d - %H:%M:%S"),
        "welcome":"This API performs an online data retrieval of Wine, Juice and Derivative production from Brasil.",
        "docs":"check /docs for usage info"
        }