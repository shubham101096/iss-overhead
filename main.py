import requests
from datetime import datetime
import smtplib
import time
import os

MY_LAT = 28.613939 # Your latitude
MY_LONG = 77.209023 # Your longitude

MY_EMAIL = os.environ.get('EMAIL')
MY_PASSWORD = os.environ.get('PASSWORD')

def is_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.
    lat_diff = round(abs(MY_LAT - iss_latitude))
    lng_diff = round(abs(MY_LONG - iss_longitude))
    if lat_diff <= 5 and lng_diff <= 5:
        return True
    else:
        return False


def is_night():

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.utcnow().hour
    if time_now <= sunrise or time_now >= sunset:
        return True
    return False

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
is_on = True

while is_on:
    if is_overhead() and is_night():
        with smtplib.SMTP("smpt.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(MY_EMAIL, MY_EMAIL, f"Subject: ISS overhead!! \n\n ")

    time.sleep(60)
