import envoy
import boto
import requests
import os
import time
from requests_oauthlib import OAuth2Session
from boto.s3.connection import Location
from boto.s3.lifecycle import Lifecycle, Transition, Rule
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler  

connected = False
connected_aws = False

KICKFLIP_API_KEY = ''
KICKFLIP_SECRET_API_KEY = ''

KICKFLIP_CLIENT_ID = ''
KICKFLIP_CLIENT_SECRET = ''

KICKFLIP_BASE_URL = 'https://funkcity.ngrok.com/'
KICKFLIP_API_URL = KICKFLIP_BASE_URL + '/api/'

AWS_ACCESS_KEY = ''
AWS_SECRET_ACCESS_KEY = ''

s3 = None

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

def connect():
    keys = load_keys()
    set_keys(key, secret_key)
    get_access_tokens()

def set_keys(client_id, client_secret):
    global KICKFLIP_CLIENT_ID
    global KICKFLIP_CLIENT_SECRET

    KICKFLIP_CLIENT_ID = client_id
    KICKFLIP_CLIENT_SECRET = client_secret

def get_access_tokens():
    global KICKFLIP_ACCESS_TOKEN
    global KICKFLIP_SECRET_ACCESS_TOKEN

    kickflip_session = OAuth2Session(KICKFLIP_ACCESS_TOKEN, token=KICKFLIP_SECRET_ACCESS_TOKEN)
    kickflip_session.authorization_url(KICKFLIP_BASE_URL + 'o/authorize/')

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

    def on_modified(self, event):
        pass

    def on_created(self, event):
        self.process(event)

def stream_video(video_path):

    create_working_directory()

    if '.avi' in video_path:
        args = "-i %s  -vcodec h264 -b 2000k -acodec libfaac -ab 128k -f hls ./.kickflip/index.m3u8"
    else:
        args = "-i %s -f hls -codec copy ./.kickflip/index.m3u8"
    args = args % video_path

    print 'ffmpeg', args

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

def upload_files(streamable_files_directory):
    return True

###################
### Misc
###################

def create_working_directory():
    if not os.path.exists('./.kickflip'):
        os.makedirs('./.kickflip')
    return True
