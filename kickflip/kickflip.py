#! /usr/bin/env python

import envoy
import boto
import requests
import os
import sys
import time
import random
import string
from requests_oauthlib import OAuth2Session
from boto.s3.connection import Location
from boto.s3.lifecycle import Lifecycle, Transition, Rule
from boto.s3.key import Key
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler  

###################
### Globals
###################

connected = False
connected_aws = False

# URLs
KICKFLIP_BASE_URL = 'https://funkcity.ngrok.com/'
KICKFLIP_API_URL = KICKFLIP_BASE_URL + '/api/'

# Kickflip Keys
KICKFLIP_CLIENT_ID = ''
KICKFLIP_CLIENT_SECRET = ''

KICKFLIP_APP_NAME = 'pythonclient'
KICKFLIP_USER_NAME = 'pythonclient-rich-jones'
KICKFLIP_ACCESS_TOKEN = ''
KICKFLIP_SECRET_ACCESS_TOKEN = ''

# Amazon
AWS_ACCESS_KEY = ''
AWS_SECRET_ACCESS_KEY = ''

s3 = None

# Video settings
VIDEO_BITRATE = '2000k'
AUDIO_BITRATE = '128k'

####################
### AWS
####################

def set_aws_keys(AWS_ACCESS_KEY_VAR, AWS_SECRET_ACCESS_KEY_VAR):
    global AWS_ACCESS_KEY
    global AWS_SECRET_ACCESS_KEY

    AWS_ACCESS_KEY = AWS_ACCESS_KEY_VAR
    AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY_VAR

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
### Kickflip Auth
###################

def connect(client_id, client_secret):
    global connected
    global KICKFLIP_CLIENT_ID
    global KICKFLIP_CLIENT_SECRET

    set_keys(client_id, client_secret)

    if not connected:

        kickflip_session = OAuth2Session(KICKFLIP_CLIENT_ID, token=KICKFLIP_CLIENT_SECRET)
        kickflip_session.authorization_url(KICKFLIP_BASE_URL + 'o/authorize/')
        import pdb
        pdb.set_trace()

        connected = True

    return connected

def set_keys(client_id, client_secret):
    global KICKFLIP_CLIENT_ID
    global KICKFLIP_CLIENT_SECRET

    KICKFLIP_CLIENT_ID = client_id
    KICKFLIP_CLIENT_SECRET = client_secret

def set_access_tokens():
    global KICKFLIP_ACCESS_TOKEN
    global KICKFLIP_SECRET_ACCESS_TOKEN

    # requests-oauth.get_tokens()
    KICKFLIP_ACCESS_TOKEN = key
    KICKFLIP_SECRET_ACCESS_TOKEN = secret_key

    return ''

####################
### Kickflip.io API
#####################

def get_account_status(username):
    return ''

def create_user(username):




    return ''

def get_user(username):
    return ''

def start_stream(file_path, stream_name=None, private=False):
    stream_video(file_path)
    return ''

def pause_stream(stream_name):
    return ''

def stop_stream():
    return ''

####################
### FFMPEG
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
        # the file will be processed there
        print event.src_path, event.event_type  # print now only for degug
        upload_file(event.src_path)

    def on_modified(self, event):
        # Do something if file is m3u8?
        if '.m3u8' in event.src_path:
            upload_file(event.src_path)

    def on_created(self, event):
        self.process(event)

def stream_video(video_path):

    global VIDEO_BITRATE
    global AUDIO_BITRATE

    create_working_directory()

    head, tail = os.path.split(video_path)
    name = tail.split('.')[0]

    nonce = '-' + ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
    
    if '.avi' in video_path:
        args = "-i %s  -vcodec h264 -b %s -acodec libfaac -ab %s -f hls ./.kickflip/%s.m3u8"
        args = args % (video_path, VIDEO_BITRATE, AUDIO_BITRATE, name+nonce)
    else:
        args = "-i %s -f hls -codec copy ./.kickflip/%s.m3u8"
        args = args % (video_path, name+nonce)

    observer = Observer()
    observer.schedule(SegmentHandler(), path='./.kickflip')
    
    observer.start()
    time.sleep(3) # This is a fucking hack.
    process = envoy.run('ffmpeg ' + args)
    observer.stop()

    upload_file(video_path)
    return ''

####################
### AWS
####################

def upload_file(file_path):

    global AWS_ACCESS_KEY
    global AWS_SECRET_ACCESS_KEY

    head, tail = os.path.split(file_path)

    bucket = None
    s3 = boto.connect_s3(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)
    bucket = s3.get_bucket(KICKFLIP_APP_NAME, validate=False)

    k = Key(bucket)
    head, tail = os.path.split(file_path)
    k.key = KICKFLIP_APP_NAME + "/"  + KICKFLIP_USER_NAME + "/" + tail

    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()

    k.set_contents_from_filename(file_path, cb=percent_cb, num_cb=10)
    if '.m3u8' in file_path:
        print k.generate_url(expires_in=300)

    return k

###################
### Misc
###################

def create_working_directory():
    if not os.path.exists('./.kickflip'):
        os.makedirs('./.kickflip')
    return True
