import envoy
import boto
import requests
from requests_oauthlib import OAuth2Session
from boto.s3.connection import Location
from boto.s3.lifecycle import Lifecycle, Transition, Rule

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

def start_stream(file_path, stream_name=None):

    stream_video(file_path)
    return ''

def pause_stream(stream_name):
    return ''

def stop_stream():
    return ''

####################
### FFMPEG
####################

def stream_video(video_path):

    args =  '-v 9 -loglevel 99 -re -i %s -an ' + \
            '-c:v libx264 -b:v 128k -vpre ipod320 \ ' + \
            ' -flags -global_header -map 0 -f segment -segment_time 4 ' + \
            ' -segment_list test.m3u8 -segment_format mpegts stream.ts'
    args = args % video_path
    process = envoy.run ('ffmpeg ' + args)

    upload_file(video_path)
    return ''

####################
### AWS
####################

def upload_files(streamable_files_directory):
    return True
