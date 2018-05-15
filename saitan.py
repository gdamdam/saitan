#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Giovanni Damiola
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import requests
import argparse
import hashlib
import archiveis
import re
import subprocess

PROGRAM_DESCRIPTION = 'This tool allows you to save a webpage with the Internet Archive Wayback Machine and archive.is. \
                       You can also download a local copy of the webpage in a WARC file and timestamp it \
                       to prove that the file existed prior to some point in time using the free service provided by opentimestamps.org. \
                       To open the WARC file we recommend to use webrecorderplayer (https://github.com/webrecorder/webrecorderplayer-electron/).'

# Configure argparser
parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
parser.add_argument('--waybackmachine', '-w', action="store_true", help="Saves [URL] to the waybackmachine")
parser.add_argument('--archiveis', '-a',  action="store_true", help="Saves [URL] to archive.is")
parser.add_argument('--localcopy', '-l',  action="store_true", help="Save [URL] locally in a WARC file.")
parser.add_argument('--opentimestamp', '-o',  action="store_true", help="Create a timestamp of the WARC file using opentimestamps.org.")
parser.add_argument('--sha256', '-s',  action="store_true", help="Returns the checksum SHA256 of the WARC file.")
parser.add_argument('url', type=str, help='[URL] to archive')
args = parser.parse_args()


def validate_url(url):
    """validates if the url is a valid url
    """
    regex = re.compile(
    r'^(?:http)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url)


def save_with_waybackmachine(url):
    """saves the url on the waybackmachine
       https://web.archive.org
    """
    url_to_save = "https://web.archive.org/save/%s" % url
    print("Saving url: {} with the waybackmachine...".format(url))
    try:
        res = requests.get(url_to_save)
        if res.status_code != 200:
            print("         sorry, something went wrong :(")
            print("Impossible to save the URL to the wayabck machine")
            wayback_location = 'FAILED'
        else:
            wayback_location = 'https://web.archive.org/'+str(res.headers['Content-Location'])
            print("WaybackMachine saved on: {}".format(wayback_location))
    except Exception as e:
        print("         sorry, something went wrong :(")
        print("Impossible to save the URL to the wayabck machine")
        wayback_location = 'FAILED'
    return wayback_location


def save_with_archiveis(url):
    """saves the page to archive.is
    """
    print("Saving url: {} with the waybackmachine...".format(url))
    try:
        archiveis_location = archiveis.capture(url)
        print("archive.is saved on: {}".format(archiveis_location))
    except Exception as e:
        print("         sorry, something went wrong :(\n {}".format(e))
        print("Impossible to save the URL to archive.is")
        archiveis_location = 'FAILED'
    return archiveis_location


def save_localcopy(url):
    """downloads locally a warc file of the url
    """
    print('Saving local copy of {}'.format(url))
    warc_filename = get_filename_from_url(url)
    try:
        subprocess.run(["wget", "-q", "-p", "-k", "-H", "--delete-after", '-e', 'robots=off', "--warc-file", warc_filename, url])
        print("WARC {}.warc.gz file saved locally.".format(warc_filename))
        warc_filename = warc_filename+'.warc.gz'
    except Exception as e:
        print("         sorry, something went wrong :(\n {}".format(e))
        print("Impossible to download the URL in a local WARC file")
        warc_filename = 'FAILED'
    return warc_filename


def get_sha256(filename):
    """returns the sha256 of the given file
       from: https://stackoverflow.com/a/22058673
    """
    BUF_SIZE = 65536
    sha256 = hashlib.sha256()
    with open(filename,'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)
    print("The checksum SHA256 for the file {} is: {}".format(filename,sha256.hexdigest()))
    outputfilename = filename+'.sha256'
    f = open(outputfilename,'w')
    f.write(sha256.hexdigest())
    f.close()
    return sha256.hexdigest()


def opentimestamp(filename):
    """submit a file to the opentimestamps.org service
    """
    print("timestamping the file {} using opetimestamps.org...".format(filename))
    try:
        subprocess.run(["ots", "stamp", filename])
        print("\nTimestamp generated!\nStore the {}.ots with the original {} for future verification.".format(filename, filename))
        fileout = filename+'.ots'
    except Exception as e:
        print("         sorry, something went wrong :(\n {}".format(e))
        fileout = 'FAILED'
    return fileout


def get_filename_from_url(url):
    """tranforms an url in a readable filename
    """
    filename = re.sub('^(?:http)s?://','',url)
    filename = re.sub(':','-',filename)
    filename = re.sub('\.','_',filename)
    filename = re.sub('\/','_',filename)
    return filename


def print_report(results):
    print('\n')
    print(80*'=')
    for i in ['waybackmachine','archiveis','localcopy','opentimestamps','sha256']:
        if i in results.keys():
            print(":: {: >16} :  {: >16}".format(i, results[i]))
    print(80*'=')


def main(url):
    """saves the url following the sets define with the arguments
    """
    results = {}
    if not validate_url(url):
        print("ERROR: {}  is not valid".format(url))
        sys.exit(1)
    if args.waybackmachine:
        results['waybackmachine'] = save_with_waybackmachine(url)
    if args.archiveis:
        results['archiveis'] = save_with_archiveis(url)
    if args.localcopy:
        results['localcopy'] = save_localcopy(url)
        if args.opentimestamp:
            results['opentimestamps'] = opentimestamp(results['localcopy'])
        if args.sha256:
            results['sha256'] = get_sha256(results['localcopy'])

    print_report(results)

if __name__ == '__main__':
    main(args.url)
