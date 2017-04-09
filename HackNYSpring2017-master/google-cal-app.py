from flask import Flask, redirect, url_for, session
from flask_oauth import OAuth
from urllib2 import Request, urlopen, URLError
import json
import datetime

# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
GOOGLE_CLIENT_ID = '484851172092-d79chvq890cl2b1lo6732fuf5gf4kma8.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'TJAt2QlBpronC1PCPgv9YcO-'
REDIRECT_URI = '/authorized'  # one of the Redirect URIs from Google APIs console

SECRET_KEY = 'development key'
DEBUG = True

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/calendar.readonly',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)

@app.route('/')
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))

    try:
        calendars = json.loads(make_request('https://www.googleapis.com/calendar/v3/users/me/calendarList'))
        events = []
        for calendar in calendars['items']:
          try:
              resp = json.loads(make_request("https://www.googleapis.com/calendar/v3/calendars/{}/events".format(calendar["id"])))

              for item in resp['items']:
                  events.append(item)
          except URLError, e:
              if e.code != 404:
                  raise e
        # filter out for today's events
        #'''
        eventName = events[0]['summary']
        eventTime = events[0]['start']['dateTime']

        return str(eventTime)
        #'''
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login'))
        return e.read()


@app.route('/login')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')


def main():
    app.run()

def make_request(url):
    access_token = session.get('access_token')
    if access_token is None:
        return False

    access_token = access_token[0]

    headers = {'Authorization': 'OAuth '+access_token}
    req = Request(url, None, headers)
    res = urlopen(req)

    return res.read()


if __name__ == '__main__':
    main()
