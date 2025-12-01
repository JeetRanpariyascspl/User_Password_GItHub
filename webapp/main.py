# pyinstaller --onefile main.py
import json, datetime
from fastapi import FastAPI, HTTPException
from webapp.jsondata import JsonData

app = FastAPI()


@app.get("/Data_JSON")
def data_json():
    json_handler = JsonData()
    try:
        data = json_handler.read_json("data.json")
        return data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="data.json not found")
    except (ValueError, json.JSONDecodeError):
        raise HTTPException(status_code=500, detail="Invalid JSON")


@app.get("/User_Password")
def user_password(ip: str, user: str, password: str):
    json_handler = JsonData()
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    json_handler.write_json("data.json", {"IP": ip, "User": user, "Password": password, "DateTime": current_datetime})
    return {"IP": ip, "User": user, "Password": password, "DateTime": current_datetime}