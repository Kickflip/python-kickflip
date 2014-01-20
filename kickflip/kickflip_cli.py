#! /usr/bin/env python

from clint.textui import colored, puts, progress
from clint import resources
import sys
import argparse
import getpass
import simplejson as json

import kickflip

def main():
    parser = argparse.ArgumentParser(description='Kickflip. Stream video directly to Kickflip.io.\n')
    parser.add_argument('file_path', metavar='U', type=str,
                        help='Path to the file to stream')
    parser.add_argument('-k', '--keys', action='store_true', default=False,
                        help='Read keys from the command line.')

    args = parser.parse_args()
    vargs = vars(args)
    if not any(vargs.values()):
        parser.error('Please supply a file to stream!')

    read_keys_cli = vargs['keys']
    client_id, client_secret = load_keys(read_keys_cli)
    user_access_key, user_access_secret_key = load_user(getpass.getuser())

    file_path = vargs['file_path']
    puts(colored.green('Streaming') + ': ' + file_path)

    #kickflip.set_keys(client_id, client_secret)
    #kickflip.set_user(resources.user)
    kickflip.start_stream(file_path)

def load_keys(read_cli=False):
    resources.init('Kickflip', 'Kickflip')
    config_json = resources.user.read('config.json')
    if not config_json:
        resources.user.write('config.json', json.dumps({}, sort_keys=True))
        config_json = resources.user.read('config.json')

    settings = json.loads(config_json)
    if not settings.has_key('client_id') or read_cli:
        settings['client_id'] = raw_input("What is your client ID? ")
        resources.user.write('config.json', json.dumps(settings, sort_keys=True))
    if not settings.has_key('client_secret') or read_cli:
        settings['client_secret'] = raw_input("What is your client secret? ")
        resources.user.write('config.json', json.dumps(settings, sort_keys=True))

    return settings['client_id'], settings['client_secret']

def load_user(username):
    resources.init('Kickflip', 'Kickflip')
    config_json = resources.user.read('config.json')
    if not config_json:
        resources.user.write('config.json', json.dumps({}, sort_keys=True))
        config_json = resources.user.read('config.json')

    settings = json.loads(config_json)
    if not settings.has_key('username'):
        settings['username'] = username
        resources.user.write('config.json', json.dumps(settings, sort_keys=True))
    if not settings.has_key('user_access_key'):
        user = kickflip.create_user(username)
        settings['user_access_key'] = 1234
        settings['user_secret_access_key'] = 1234
        resources.user.write('config.json', json.dumps(settings, sort_keys=True))

    return settings['user_access_key'], settings['user_secret_access_key']

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception, e:
        print e
