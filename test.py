from twilio.rest import TwilioRestClient
from datetime import datetime
import time
import forecast
import nytimesapi
import googleCalApp

# Your Account SID from twilio.com/console
account_sid = "ACd462406da1770f0815a80eb4a74ffc40"
# Your Auth Token from twilio.com/console
auth_token  = "22dc45c5e28d04abe7fb277b75d3affc"

client = TwilioRestClient(account_sid, auth_token)
now = datetime.now()
# timeToday = str(now.hour) + ": " + str(now.minute)

'''
now.second
time.sleep(5)
datetime.now().second
'''



note = "Good morning Nick! /n"
# forecast data
# note +=  forecast.forecast(10003) + "/n"
note += nytimesapi.news()
note += googleCalApps
print(note)





def execute():
    call = client.calls.create(to="+13473366702",
                                   from_="+13476573267",
                                   url="http://54.212.203.160/source/voice.xml")


    message = client.messages.create(
            to="+13473366702",
            from_="+13476573267",
            body=note)
    print(call.sid)
    print(message.sid)

execute()
