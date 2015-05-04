#! /usr/bin/env python

import envoy
import boto
import requests
import os
import sys
import time
import random
import string
from oauthlib.oauth2 import MobileApplicationClient
from requests_oauthlib import OAuth2Session
from boto.s3.connection import Location
from boto.s3.lifecycle import Lifecycle, Transition, Rule
from boto.s3.key import Key
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from m3u8 import M3U8

###################
# Globals
###################

connected = False
connected_aws = False
kickflip_session = None

# URLs
KICKFLIP_BASE_URL = 'https://funkcity.ngrok.com/'
# KICKFLIP_BASE_URL = 'https://api.kickflip.io'
KICKFLIP_API_URL = KICKFLIP_BASE_URL + '/api/'

# Kickflip Keys
KICKFLIP_CLIENT_ID = ''
KICKFLIP_CLIENT_SECRET = ''

KICKFLIP_APP_NAME = ''
KICKFLIP_USER_NAME = ''
KICKFLIP_UUID = ''
KICKFLIP_ACCESS_TOKEN = ''
KICKFLIP_SECRET_ACCESS_TOKEN = ''

# Amazon
AWS_ACCESS_KEY = ''
AWS_SECRET_ACCESS_KEY = ''

s3 = None

# Video settings
VIDEO_BITRATE = '2000k'
AUDIO_BITRATE = '128k'

playlist = M3U8()

####################
# AWS
####################


def set_aws_keys(USERNAME, AWS_ACCESS_KEY_VAR, AWS_SECRET_ACCESS_KEY_VAR):
    global AWS_ACCESS_KEY
    global AWS_SECRET_ACCESS_KEY
    global KICKFLIP_USER_NAME

    AWS_ACCESS_KEY = AWS_ACCESS_KEY_VAR
    AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY_VAR
    KICKFLIP_USER_NAME = USERNAME

    return True


def connect_aws():

    global connected_aws
    global AWS_ACCESS_KEY
    global AWS_SECRET_ACCESS_KEY
    global s3

    if not connected_aws:
        s3 = boto.connect_s3(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)
        connected_aws = True

    return connected_aws


def upload_file(filename):
    return True


###################
# Kickflip Auth
###################


def connect():
    global connected
    global kickflip_session
    global KICKFLIP_CLIENT_ID
    global KICKFLIP_CLIENT_SECRET
    global KICKFLIP_API_URL

    if not connected:

        endpoint = KICKFLIP_BASE_URL + '/o/token/'

        payload = ({
            'client_secret': KICKFLIP_CLIENT_SECRET,
            'grant_type': 'client_credentials',
            'client_id': KICKFLIP_CLIENT_ID,
            })

        response = requests.post(endpoint, payload)

        if response.status_code != 200:
            raise Exception("Error: Couldn't connect to Kickflip...")

        token = response.json()

        client = MobileApplicationClient(KICKFLIP_CLIENT_ID)

        kickflip_session = OAuth2Session(
            KICKFLIP_CLIENT_ID,
            client=client,
            token=token
        )

        connected = True
        print "CONNECTED"

    return connected


def auth_required(f):
    global connected
    global kickflip_session

    def g(*args, **kwargs):
        if not connected:
            raise Exception("No session connected. connect() first?")
        return f(*args, **kwargs)

    return g


def set_keys(client_id, client_secret):
    global KICKFLIP_CLIENT_ID
    global KICKFLIP_CLIENT_SECRET

    KICKFLIP_CLIENT_ID = client_id
    KICKFLIP_CLIENT_SECRET = client_secret


def set_uuid(uuid):

    global KICKFLIP_UUID
    KICKFLIP_UUID = uuid

    return True


def set_access_tokens():
    global KICKFLIP_ACCESS_TOKEN
    global KICKFLIP_SECRET_ACCESS_TOKEN

    # requests-oauth.get_tokens()
    KICKFLIP_ACCESS_TOKEN = key
    KICKFLIP_SECRET_ACCESS_TOKEN = secret_key

    return ''

####################
# Kickflip.io API
#####################


def get_account_status(username):
    return ''


@auth_required
def create_user(username, password=""):
    """
    Uses the `/user/new` endpoint taking the username as a parameter.

    TODO: What happens when you specify no password?

    e.g. username="banana1"

    """
    endpoint = KICKFLIP_API_URL + '/user/new'
    payload = {'username': username}

    if password:
        payload['password'] = password

    user_response = kickflip_session.post(endpoint, payload)

    return user_response.json()


@auth_required
def get_user_info(username):
    """
    Uses the `/user/info` endpoint taking the username as a parameter.

    e.g. username="banana1"

    """
    endpoint = KICKFLIP_API_URL + '/user/info/'
    payload = {'username': username}

    user_response = kickflip_session.post(endpoint, payload)

    return user_response.json()


def get_user(username):
    return ''


def start_stream(file_path, stream_name=None, private=False, username=''):
    """
    Uses the `/stream/start` endpoint taking the username as a parameter.
    If you specify no username, it will fallback to the default
    `KICKFLIP_USER_NAME` set in the set_aws_keys() function.

    e.g. username="banana1"

    """
    endpoint = KICKFLIP_API_URL + '/stream/start/'
    payload = {'username': KICKFLIP_USER_NAME}

    if username:
        payload['username'] = username

    user_response = kickflip_session.post(endpoint, payload)

    import pdb
    pdb.set_trace()
    stream_video(file_path)
    return ''


def pause_stream(stream_name):
    return ''


def stop_stream():
    return ''


@auth_required
def get_stream_info(stream_id):
    """
    Uses the `/stream/info` endpoint taking the stream_id as a parameter.

    e.g. stream_id="e83a515e-fe69-4b19-afba-20f30d56b719"

    """
    endpoint = KICKFLIP_API_URL + '/stream/info/'
    payload = {'stream_id': stream_id}

    response = kickflip_session.post(endpoint, payload)

    return response.json()


@auth_required
def get_stream_by_location(uuid, lat, lon, radius=0):
    """
    Uses the `/search/location` endpoint.
    takes the stream_id as a parameter.

    e.g. uuid="", username="bej48snvvthy"

    """
    endpoint = KICKFLIP_API_URL + '/search/location/'
    payload = ({
        'uuid': uuid,
        'lat': lat,
        'lon': lon
    })

    if radius != 0:
        payload['radius'] = radius

    response = kickflip_session.post(endpoint, payload)

    return response.json()


@auth_required
def get_stream_credentials(username, password):
    """
    Uses the `/user/uuid` endpoint.
    takes a valid username and password as parameter.
    It will return all the necessary credentials to use the API
    and the upload endpoints.

    e.g. username="bej48snvvthy", password=""

    """
    endpoint = KICKFLIP_API_URL + '/user/uuid/'
    payload = {'username': username, 'password': password}

    response = kickflip_session.post(endpoint, payload)

    return response.json()


@auth_required
def search_by_keyword(keyword="", uuid=""):
    """
    Uses the `/search` endpoint.
    takes a user uuid and a keyword.
    If you specify no `uuid`, the search will not show private streams?
    If the keyword is empty, it will return all the streams from the app.

    e.g. uuid="e9c3d27e-406b-4f4a-9b87-6d3460c60ca6", keyword=""

    reply: {
        u'total_items': 3,
        u'next_page_available': False,
        u'success': True, u'page_number': 1,
        u'streams': [...],
        u'results_per_page': 25
    }

    """
    endpoint = KICKFLIP_API_URL + '/search/'
    payload = {'uuid': uuid, 'keyword': keyword}

    response = kickflip_session.post(endpoint, payload)

    return response.json()


####################
# FFMPEG
####################


class SegmentHandler(PatternMatchingEventHandler):
    patterns = ["*.ts", "*.m3u8"]

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # Process the file there
        print event.src_path, event.event_type  # Print for degug

        if '.m3u8' not in event.src_path:
            upload_file(event.src_path)

    def on_modified(self, event):

        global playlist

        if '.m3u8' in event.src_path:
            playlist.add_from_file(event.src_path)
            playlist.dump_to_file(event.src_path + '.complete.m3u8')
            upload_file(event.src_path + '.complete.m3u8')

    def on_created(self, event):
        self.process(event)


def stream_video(video_path):

    global VIDEO_BITRATE
    global AUDIO_BITRATE

    create_working_directory()

    head, tail = os.path.split(video_path)
    name = tail.split('.')[0]

    alphanum = string.ascii_uppercase + string.digits

    nonce = '-' + ''.join(random.choice(alphanum) for x in range(5))

    if '.avi' in video_path:
        args = "-i %s  -vcodec h264 "
        args += "-b %s -acodec libfaac"
        args += "-ab %s -f hls ./.kickflip/%s.m3u8"
        args = args % (video_path, VIDEO_BITRATE, AUDIO_BITRATE, name+nonce)
    else:
        args = "-i %s -f hls -codec copy ./.kickflip/%s.m3u8"
        args = args % (video_path, name+nonce)

    observer = Observer()
    observer.schedule(SegmentHandler(), path='./.kickflip')

    observer.start()
    time.sleep(3)  # This is a fucking hack.
    process = envoy.run('ffmpeg ' + args)
    observer.stop()

    upload_file(video_path)
    return ''


####################
# AWS
####################


def upload_file(file_path):

    global AWS_ACCESS_KEY
    global AWS_SECRET_ACCESS_KEY

    head, tail = os.path.split(file_path)

    bucket = None
    s3 = boto.connect_s3(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)
    bucket = s3.get_bucket(KICKFLIP_APP_NAME)  # , validate=False)

    k = Key(bucket)
    head, tail = os.path.split(file_path)
    k.key = KICKFLIP_USER_NAME + "/" + tail

    k.set_contents_from_filename(file_path)
    k.set_acl('public-read')
    if '.m3u8' in file_path:
        print k.generate_url(expires_in=300)

    return k


###################
# Misc
###################


def create_working_directory():
    if not os.path.exists('./.kickflip'):
        os.makedirs('./.kickflip')
    return True
