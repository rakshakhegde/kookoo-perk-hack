"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
import flask
from flask import Flask
import xml.etree.cElementTree as ET
import logging
import urllib
from google.appengine.api import urlfetch
import json
from random import randint
from uber_rides.session import Session
import time

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

# Twilio/Kookoo XML variables
RESPONSE = 'Response'
SAY = 'playtext'  # Twilio: Say; Kookoo: playtext
HANGUP = 'hangup'  # Kookoo: hangup
TAG_RECORD = 'record'
EVENT_RECORD = 'Record'
NEW_CALL = 'NewCall'
DISCONNECT = 'Disconnect'
EVENT_HANGUP = 'Hangup'
TAG_HANGUP = 'hangup'

# Sample mp3: http://recordings.kookoo.in/rakshakhegde/info_now.mp3

ext1 = '_50'
ext2 = '_51'
ext3 = '_52'
ext4 = '_53'

type=-1

@app.route('/')
def kookooSIP():
	reqargs = flask.request.args
	event = reqargs.get('event')
	response = None
	if event == NEW_CALL or not event:
		response = newCall(reqargs)
	elif event == EVENT_RECORD:
		response = recordEvent(reqargs)
	else:
		response = hangup()
	xmlOutput = ET.tostring(response, encoding='utf8', method='xml')
	return xmlOutput, 200, {'Content-Type': 'application/xml; charset=utf-8'}


def newCall(args):
	cid = args.get('cid')
	response = ET.Element(RESPONSE)
	ET.SubElement(response, SAY).text = 'Query'
	ET.SubElement(response, TAG_RECORD, {'format': 'wav', 'maxduration': '3'}).text = cid + ext1
	return response


def getS2T(src):
	baseUrl = 'http://52.24.112.182:8080/s2t?src='
	urlfetch.set_default_fetch_deadline(50)
	time.sleep(3)
	recResult = urlfetch.Fetch(baseUrl + src)
	content = recResult.content
	logging.debug(content)
	return content


def recordEvent(args):
	return makeSense(getS2T(args.get('cid') + ext1))


def makeSense(transcript):
	logging.debug(transcript)
	logging.debug('Transcript is: ' + transcript)
	if ('uber' or 'taxi' or 'car' or 'cab') in transcript:
		return bookUber()
	elif ('food' or 'khana') in transcript:
		return bookFood()
	else:
		return anythingElse()


# Services, finally, YAY ^_^
def bookUber():
	args = flask.request.args
	cid = args.get('cid')
	response = ET.Element(RESPONSE)
	ET.SubElement(response, SAY).text = 'Booking an Uber taxi. State your pickup and end location'
	ET.SubElement(response, TAG_RECORD, {'format': 'wav', 'maxduration': '3'}).text = cid + ext2
	ET.SubElement(response, 'gotourl').text = 'http://kookoo-1161.appspot.com/uber1'
	return response


@app.route('/uber1')
def uber1():
	args = flask.request.args
	cid = args.get('cid')
	pickLoc = 'Electronic City'
	endLoc = 'Majestic'
	response = ET.Element(RESPONSE)
	ET.SubElement(response, SAY).text = 'You will be picked up from'
	ET.SubElement(response, SAY).text = pickLoc
	ET.SubElement(response, SAY).text = 'and dropped off at'
	ET.SubElement(response, SAY).text = endLoc
	ET.SubElement(response, SAY).text = pickLoc
	ET.SubElement(response, SAY).text = 'and dropped off at'
	ET.SubElement(response, SAY).text = endLoc
	ET.SubElement(response, SAY).text = 'Please wait'
	ET.SubElement(response, 'playaudio').text = 'https://dl2.pushbulletusercontent.com/orAPQ5EltMnhdwCzbfx3DuUnhaN1yTV5/output.mp3'
	fare = 263 if randint(0, 1) else 346
	ET.SubElement(response, SAY).text = 'Your total fare is'
	ET.SubElement(response, 'say-as', {'format': '402', 'lang': 'EN'}).text = str(fare)
	ET.SubElement(response, SAY).text = 'Details of the driver will be sent by SMS to you. Have a happy journey.'
	xmlOutput = ET.tostring(response, encoding='utf8', method='xml')
	ET.SubElement(response, TAG_HANGUP)
	type=0
	return xmlOutput, 200, {'Content-Type': 'application/xml; charset=utf-8'}

def bookFood():
	response = ET.Element(RESPONSE)
	args = flask.request.args
	cid = args.get('cid')
	response = ET.Element(RESPONSE)
	ET.SubElement(response, SAY).text = 'What would you like to eat?'
	ET.SubElement(response, TAG_RECORD, {'format': 'wav', 'maxduration': '2'}).text = cid + ext3
	getS2T(cid + ext3)
	ET.SubElement(response, SAY).text = 'Pizza confirmed'
	ET.SubElement(response, SAY).text = 'Any particular toppings you would like?'
	ET.SubElement(response, TAG_RECORD, {'format': 'wav', 'maxduration': '2'}).text = cid + ext4
	getS2T(cid + ext4)
	ET.SubElement(response, SAY).text = 'Would you like pickup or delivery?'
	ET.SubElement(response, TAG_RECORD, {'format': 'wav', 'maxduration': '2'}).text = cid + ext4
	ET.SubElement(response, SAY).text = 'You can pick up your'
	ET.SubElement(response, SAY).text = 'Pizza'
	ET.SubElement(response, SAY).text = 'at your nearest Dominos'
	ET.SubElement(response, SAY).text = 'Please wait'
	ET.SubElement(response, 'playaudio').text = 'https://dl2.pushbulletusercontent.com/orAPQ5EltMnhdwCzbfx3DuUnhaN1yTV5/output.mp3'
	ET.SubElement(response, SAY).text = 'Your total price is'
	fare = 250 if randint(0, 1) else 300
	ET.SubElement(response, 'say-as', {'format': '402', 'lang': 'EN'}).text = str(fare)
	ET.SubElement(response, SAY).text = 'Details will be sent as SMS to you. Bye.'
	xmlOutput = ET.tostring(response, encoding='utf8', method='xml')
	ET.SubElement(response, TAG_HANGUP)
	type=1
	return response


def anythingElse():
	response = ET.Element(RESPONSE)
	ET.SubElement(response, SAY).text = 'Some other awesome service'
	return response


def hangup():
	if type==0:
		urlfetch.Fetch('http://www.kookoo.in/outbound/outbound_sms.php?phone_no='+cid+'&api_key=KK268a2e81e84db444386421ac2d771fd8&message=You+will+be+picked+up+by+Ravindra+Raju+His+contact+number+is+09886598645.+Expect+arrival+within+15+mins.%0D%0ABon+Voyage+%3A%29&senderid=KOOKOO')
	elif type==1:
		urlfetch.Fetch('http://www.kookoo.in/outbound/outbound_sms.php?phone_no='+cid+'&api_key=KK268a2e81e84db444386421ac2d771fd8&message=Pick+up+your+pizza+at+Dominos%2C+3rd+Main+Road%2C+Koramangala%0D%0ABon+Appetite+%3A%29&senderid=KOOKOO')


@app.errorhandler(404)
def page_not_found(e):
	"""Return a custom 404 error."""
	return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
	"""Return a custom 500 error."""
	return 'Sorry, unexpected error: {}'.format(e), 500
