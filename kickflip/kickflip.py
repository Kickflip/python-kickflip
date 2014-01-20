import boto
from boto.s3.connection import Location
from boto.s3.lifecycle import Lifecycle, Transition, Rule

connected = False

KICKFLIP_API_KEY = ''
KICKFLIP_SECRET_API_KEY = '' 

KICKFLIP_ACCESS_TOKEN = ''
KICKFLIP_SECRET_ACCESS_TOKEN = '' 

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

    global connected
    global AWS_ACCESS_KEY
    global AWS_SECRET_ACCESS_KEY
    global s3

    if not connected:
        s3 = boto.connect_s3(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)
        connected = True

    return connected

def upload_file(filename):
    return True

###################
### Kickflip Auth
###################

def set_keys(key, secret_key):
    global KICKFLIP_API_KEY
    global KICKFLIP_SECRET_API_KEY

    KICKFLIP_API_KEY = key
    KICKFLIP_SECRET_API_KEY = secret_key

def get_access_tokens():
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

def start_stream(stream_name):
    return ''

def pause_stream(stream_name):
    return ''

def stop_stream():
    return ''

####################
### FFMPEG
####################

def stream_video(video_path):
    upload_file(video_path)
    return ''