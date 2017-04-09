from flask import *
from flask_oauth import OAuth
from urllib2 import Request, urlopen, URLError
import json
import time

from forecast import *
import gcalendar
import nyt
from utils import *

oauth = OAuth()

KEYS = json.loads(open('app/.GAPI_KEYS.json').read())
GOOGLE_CLIENT_ID = KEYS['G_CLIENT_ID']
GOOGLE_CLIENT_SECRET = KEYS['G_CLIENT_SECRET']
REDIRECT_URI = '/authorized'  # one of the Redirect URIs from Google APIs console

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

core = Blueprint('core', __name__)

@core.route('/')
def home():
	return render_template('index.html')

@core.route('/dashboard')
def dash():
	return render_template('dashboard.html')

@core.route('/login')
def login():
	callback=url_for('core.authorized', _external=True)
	return google.authorize(callback=callback)

@core.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('core.home'))

@core.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
	access_token = resp['access_token']
	session['access_token'] = access_token, ''
	return redirect(url_for('core.calendar'))


@google.tokengetter
def get_access_token():
	return session.get('access_token')


def make_request(url):
	access_token = session.get('access_token')
	if access_token is None:
		return False

	access_token = access_token[0]

	headers = {'Authorization': 'OAuth '+access_token}
	req = Request(url, None, headers)
	res = urlopen(req)

	return res.read()

@core.route('/forecast')
def forecast():
	return get_forecast(11201)

@core.route('/news')
def news():
	return nyt.news()

@core.route('/calendar')
def calendar():
	access_token = session.get('access_token')
	if access_token is None:
		return redirect(url_for('core.login'))

	try:
		calendars = json.loads(make_request('https://www.googleapis.com/calendar/v3/users/me/calendarList'))
		events = []
		for calendar in calendars['items']:
			try:
				resp = json.loads(make_request("https://www.googleapis.com/calendar/v3/calendars/{}/events".format(calendar["id"])))
				for item in resp['items']:
					events.append(item)
			except URLError, e:
				return "Unable to access Google calendar"
			events_dict = todayEvents(events)
			return str(events_dict)
	except:
		return "Error occurred"