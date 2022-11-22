from fastapi import APIRouter, Depends
from datetime import datetime

from Controllers.AuthController import User, get_current_user

controllerName = "date"
dateController = APIRouter()

@dateController.get(f'/{controllerName}/currentTime')
def getCurrentDate(user: User = Depends(get_current_user)):
    return f"{datetime.now()}", 200
