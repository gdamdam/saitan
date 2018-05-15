# saitan - v1.0

Saintan allows you to save a webpage from the Internet to a web archiving tool like the Internet Archive's [Wayback Machine](https://web.archive.org/) and [archive.is](https://archvie.is).
Saitan allows you also to download a local copy of the page, and all its components in a [WARC](https://en.wikipedia.org/wiki/Web_ARChive) file, calculate its [checksum](https://en.wikipedia.org/wiki/Checksum) SHA256 and [timestamp](https://en.wikipedia.org/wiki/Timestamp) it to prove that the file  existed prior to some point in time using the free service provided by [opentimestamps.org](https://opentimestamps.org).
To open the WARC file we recommend to use [webrecorderplayer](https://github.com/webrecorder/webrecorderplayer-electron).


## Installation

To run this script you need python3, clone this repository and install some extra packages

    git clone
    cd saitan
    pip3 install -r requirements.txt

You need also to have _*wget*_ installed in you machine.


## Usage

To save the page http://example.com on the Wayback Machine you can use:

    python3 saitan.py -w http://exemple.com

to save it on _archive.is_:

    python3 saitan.py -a http://exemple.com

to save a local copy in a WARC file:

    python3 saitan.py -l http://example.com

You can save the page in several place with a single command concatenating the arguments.
To save a page on the wayback machine, archive.is and in a local WARC file:

    python saitan.py -lwa http://example.com

To timestamp the WARC file using opentimestamps.org you can type:

    python3 saitan.py -lo http://example.com

To see a complete list of the available arguments you can type:

    python3 saitan.py -h

    optional arguments:
    -h, --help            show this help message and exit
    --waybackmachine, -w  Saves [URL] to the waybackmachine
    --archiveis, -a       Saves [URL] to archive.is
    --localcopy, -l       Save [URL] locally in a WARC file.
    --opentimestamp, -o   Create a timestamp of the WARC file using opentimestaps.org
    --sha256, -s          Returns the checksum SHA256 of the WARC file.


## Open the WARC file

To open the WARC file we recommend to use [Webrecorder Player](https://github.com/webrecorder/webrecorderplayer-electron/).


## Verify the timestamp

The file timestamped and the timestamp file _.ots_ must be stored together to allow future verification.
To verify the timestamp you can use the form on the website https://opentimestamps.org
Remember that it takes a few hours for the timestamp to get confirmed by the Bitcoin blockchain.


## License (GPLv3)

Copyright (C) 2018 saitan developers.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
