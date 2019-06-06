#!/usr/bin/env python3
# -*- coding: utf-8-*-

import sys
from dateutil import parser
from datetime import datetime, timedelta

""" Log Parser for Kart races """

Class Pilot:
    nowPrefix=datetime.now().strftime("%Y-%m-%d")
    all_pilots={} # we need to track our instances. A data dictionary is ideal for this

    def __init__(self, name, code):
        self.name=name
        self.code=code
        self.best_lap_time=timedelta(0)
        self.max_lap=0
        self.latest_lap_time=timedelta(0)
        self.position=0
        self.total_time=timedelta(0)
        self.average_speed=0.0
        all_pilots[self.code + " - " + self.name]=self # so that we can find by code and name


    def bestLap(self):
        True

    def averageSpeed(self):

    def timeDifference(self, totaltime):

def parse_line(fline):
    """
    Transforms each text line in an array of typed elements.
    >>> parse_line("23:49:08.277      038 - F.MASSA                           11:02.852                        44,275")

    """
    elements=fline.split()

    # Basic consistency check
    # second condition for len > 2 prevents an index error in the next one
    if len(elements) != 7 or (len(elements)>2 and elements[2]!="-"):
        return [None,'','','',0,timedelta(0),0.0]

"""
    fields:
    1 - time of lap
    2 - code
    3 - "-"
    4 - name
    5 - lap number
    6 - time of lap, MM:SS.FFF
    7 - average speed, float with commas
"""
    

    
def parse_date(datestring):
    return datetime.strptime(Pilot.nowPrefix+' '+datestring,"%Y-%m-%d %H:%M:%S.%f")
    

def kartparser():
    """
    Main program: parser an user-provided log file
    >>> sys.argv=['kartparser']; kartparser()
    Usage: python3 kartparser <logfile>
    2
    >>> sys.argv=['kartparser','/dev/nothing']; kartparser()
    Error reading file /dev/nothing, please check
    Error message:  [Errno 2] No such file or directory: '/dev/nothing'
    3
    """

    if len(sys.argv) < 2:
        print(f'Usage: python3 {sys.argv[0]} <logfile>')
        return 2

    inputfile=sys.argv[1]

    try:
        f = open(inputfile, 'r')
    except:
        print(f'Error reading file {inputfile}, please check')
        print(f'Error message: ',sys.exc_info()[1])
        return 3

    # Skip the first line
    f.reafline()

    # main loop for gobbling up data
    while fline in f.reaflines():
        elements=parse_line(fline)

if __name__ == "__main__":
   sys.exit(kartparser())
