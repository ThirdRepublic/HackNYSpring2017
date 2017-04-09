# utility parsing junk
from twilio.rest import Client
from datetime import datetime
import json

KEYS = json.loads(open('app/.TWILIO_KEYS.json').read())
SID = KEYS['SID']
AUTH_TOKEN = KEYS['TOKEN']
client = Client(SID, AUTH_TOKEN)

def todayEvents(events):

    """returns dict of events today with their time.

    precondition: events is a list of dictionaries from GoogleCal"""

    now = datetime.now()
    timeMin = datetime(year=now.year, month=now.month, day=now.day, hour = 0, minute = 0, second = 0)
    timeMin = timeMin.isoformat()
    timeMax = datetime(year=now.year, month=now.month, day=now.day, hour = 23, minute = 59, second = 59)
    timeMax = timeMax.isoformat()

    

    todayEvents = []
    eventNames = []
    for i in range(0,len(events)-1):
        eventTime = events[i]['start']['dateTime']
        date_ind = eventTime.find('T') #where date ends, i.e. where the T is
        eventTime_date = eventTime[:date_ind] # just the date
        eventTime_time = eventTime[date_ind+1:] # just the time
        timeMin_date = timeMin[:date_ind]

        if timeMin_date == eventTime_date:
            todayEvents.append({(events[i]['summary']):eventTime_time})
            eventNames.append(events[i]['summary'])
    return todayEvents

    # for text messages to get schedule, for loop todayEvents. example:
    # eventNames[0] // name of event
    # todayEvents[0][eventNames[0]] // time of event

def send(to_, from_, msg):
    call = client.calls.create(to=to_,
                                   from_=from_,
                                   url="app/static/xml/voice.xml")


    message = client.messages.create(
            to=to_,
            from_=from_,
            body=msg)


    
