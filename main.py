# Before to run this program this program run this commands:
# python3 -m venv venv
# pip3 install requests
import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL = "" #Put your email here
MY_PASSWORD = "" #Put your AppPassword (take a look in google account -> Security --> App Password)
# To get your coordinates follow this link: https://www.latlong.net/
MY_LAT = # Your latitude
MY_LONG = # Your longitude

def is_iss_overhead():
    """ This function decect the position in real time of the ISS and check if is at our same coordinates. """
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True
    return False

def is_night():
    """ This function check if is night. """
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
    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True
    else: 
        return False

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        # Send an email if the ISS is over your position
        connection = smtplib.SMTP("__YOUR_SMTP_ADDRESS_HERE___")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:Look Up👆\n\nThe ISS is above you in the sky."
        )