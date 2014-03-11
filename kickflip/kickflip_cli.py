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
    parser.add_argument('-s', '--shell', action='store_true', default=False,
                        help='Open a shell with a kickflip session connected.')

    args = parser.parse_args()
    vargs = vars(args)
    if not any(vargs.values()):
        parser.error('Please supply a file to stream!')

    read_keys_cli = vargs['keys']
    client_id, client_secret = load_keys(read_keys_cli)

    file_path = vargs['file_path']

    kickflip.set_keys(client_id, client_secret)
    print "Connecting.."
    kickflip.connect()

    print "Loading user.."
    load_or_create_user(getpass.getuser())

    if vargs['shell']:
        puts(colored.green('Here\'s your shell!'))
        
        import pdb
        pdb.set_trace()
    else:
        puts(colored.green('Streaming') + ': ' + file_path)
        kickflip.start_stream(file_path)

def load_keys(read_cli=False):
    resources.init('Kickflip', 'Kickflip')
    config_json = resources.user.read('config.json')
    if not config_json:
        resources.user.write('config.json', json.dumps({}, sort_keys=True))
        config_json = resources.user.read('config.json')

    settings = json.loads(config_json)
    
    # Nuke the settings if reading from CLI.
    if read_cli:
        settings = {}

    if not settings.has_key('client_id') or read_cli:
        settings['client_id'] = raw_input("What is your client ID? ").strip()
        resources.user.write('config.json', json.dumps(settings, sort_keys=True))
    if not settings.has_key('client_secret') or read_cli:
        settings['client_secret'] = raw_input("What is your client secret? ")
        resources.user.write('config.json', json.dumps(settings, sort_keys=True))

    return settings['client_id'], settings['client_secret']

def load_or_create_user(username):
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
        settings['username'] = user['name']
        settings['user_access_key'] = user['aws_access_key']
        settings['user_secret_access_key'] = user['aws_secret_key']
        settings['user_uuid'] = user['uuid']
        resources.user.write('config.json', json.dumps(settings, sort_keys=True))

    kickflip.set_aws_keys(settings['username'], settings['user_access_key'], settings['user_secret_access_key'])
    kickflip.set_uuid(settings['user_uuid'])

    return settings['username'], settings['user_uuid'], settings['user_access_key'], settings['user_secret_access_key']

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception, e:
        print e
