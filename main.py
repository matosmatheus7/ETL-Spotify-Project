from sqlalchemy.orm import sessionmaker
import requests
from datetime import datetime
import datetime


DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
USER = "matosmatheux"
TOKEN = "BQB2xjzmGz2-exz96MMDPsAVnSZryMTP3_XmrvaFCOvKJ8zDmg_ag6gt2Eg5a7GHkuAfYMjsa9gz-NiINuoj4zUZhfFoaOTLIV2xNsKdWTnXFI3J3P1lTqrF1ZOxja6qbfwnkrke4_Uh620mD26vktZqOUU"

if __name__ == "__main__":

    # Extract part of the ETL process
 
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }
    
    # Convert time to Unix timestamp in miliseconds      
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # Download all songs you've listened to "after yesterday", which means in the last 24 hours      
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers = headers)

    data = r.json()

    print(data)
