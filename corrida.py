#!/usr/bin/env python3
# -*- coding: utf-8-*-

import sys
from datetime import datetime, timedelta
from collections import OrderedDict

""" Log Parser for Kart races """

class Pilot:
    nowPrefix="2019-01-01"  # this prefix will be fixed since class is declared
    _all_pilots = {}  # we need to track our instances. A data dictionary keyed by code + name is ideal for this

    _maximum_lap = 4  # race will finish when max_lap get to this number
    _best_overall_lap = timedelta.max
    _total_race_time = timedelta(0)  # timedelta.min is negative, not gonna risk inconsistencies

    def __init__(self, code, name):
        self.name = name
        self.start_time = None
        self.end_time = None
        self.time_dif_first_place = None
        self.code=code
        self.best_lap_time = timedelta.max
        self.max_lap = 0
        self.latest_lap_time = timedelta(0)
        self.position = 0
        self.total_time = timedelta(0)
        self.average_speed = 0.0
        self.valid = False
        self.current_hour = None
        self.finished = True
        Pilot._all_pilots[self.code + " - " + self.name] = self  # so that we can find by code and name
        return None

    def add_lap(self, lap_hour, lap_number, lap_duration, average_lap_speed):
#        print ("add_lap: " +str(self.max_lap) + " " + str(lap_hour) + " " + str(lap_number) + " " + str(lap_duration.total_seconds()) + " " + str(average_lap_speed))
        if self.max_lap == int(lap_number) - 1: # Consecutive laps are enforced
            self.max_lap = int(lap_number)
            self.current_hour = lap_hour
            if self.max_lap == 1: # First time? Let's initialize some values!
                self.start_time = lap_hour - lap_duration
                self.best_lap_time = lap_duration
                self.total_time = lap_duration
                self.average_speed = average_lap_speed
                self.valid = True # we should do that only once per pilot
            else:
                if self.max_lap == Pilot._maximum_lap:
                    self.finished = True
                    self.end_time = lap_hour

                # new average speed is going to be total_distance / total_time
                total_distance = (float(average_lap_speed) * lap_duration.total_seconds()) + \
                              (self.average_speed * self.total_time.total_seconds() )
                # and now the average speed calculation
                self.total_time = self.total_time + lap_duration
                self.average_speed = float(total_distance / self.total_time.total_seconds())
                # we used the previous total_time, now we can update it:

            if self.best_lap_time > lap_duration:
                self.best_lap_time = lap_duration

            return True

        else:
            self.valid=False
            print(f'*** INCONSISTENT LAP NUMBER FOR ' + self.code + f' - ' + self.name)
            return False

    @classmethod
    def update_finished(cls):
        # first, let's order them by total_time and substitute the dictionary!
        # python 3 guarantess order of inclusion of dicts with OrderedDict
        if len(Pilot._all_pilots) == 0:
            print(f'No elements in list')
            return False
        # Transform our dict of pilots in an ordered dict, sorted by laps (descending) and total time of race,
        # less time means being first if all laps were completed.
        Pilot._all_pilots=OrderedDict(sorted(Pilot._all_pilots.items(), \
                          key=lambda x: ((Pilot._maximum_lap - x[1].max_lap), x[1].total_time.total_seconds())))
        pos_tmp=1
        pilot = None
        firstpilot = None
        for pilot in Pilot._all_pilots.values():
            pilot.position=pos_tmp
            if pilot.position == 1:
                firstpilot = pilot
            pos_tmp = pos_tmp + 1
            if pilot.max_lap < Pilot._maximum_lap:
                pilot.finished = False
            else:
                pilot.finished = True
            if pilot.best_lap_time < Pilot._best_overall_lap and pilot.finished:
                Pilot._best_overall_lap = pilot.best_lap_time
            if pilot.total_time > Pilot._total_race_time:
                Pilot._total_race_time = pilot.total_time
            pilot.time_dif_first_place = pilot.total_time - firstpilot.total_time
            pilot.end_time = pilot.current_hour 
        return True

    @classmethod
    def best_lap_time(cls):
        if Pilot._best_overall_lap < timedelta.max:
            return Pilot._best_overall_lap
        else:
            print(f'Best lap time not yet calculated, run Pilot.update_finished()')
            return timedelta(0)

    @classmethod
    def total_time(cls):
        if Pilot._total_race_time == timedelta(0):
            print(f'Total race time not yet calculated, run Pilot.update_finished()')
        return Pilot._total_race_time

    @classmethod
    def get_pilot(cls, code, name):
        tmp_pilot=None
        try:
            tmp_pilot = Pilot._all_pilots[code + " - " + name]
        except KeyError:
            tmp_pilot=None
        return tmp_pilot

    @classmethod
    def all_pilots(cls):
        return Pilot._all_pilots.values()

    @classmethod
    def best_lap(cls):
        return Pilot._best_overall_lap

    @classmethod
    def total_time(cls):
        return Pilot._total_race_time

def parse_line(fline):
    """
    Transforms each text line in an array of typed elements. Excludes the "-".
    >>> parse_line("")
    [None, '', '', '', 0, datetime.timedelta(0), 0.0]
    >>> parse_line("23:49:08.277      038 - F.MASSA                           1            1:02.852                        44,275")
    [datetime.datetime(2019, 1, 1, 23, 49, 8, 277000), '038', 'F.MASSA', 1, datetime.timedelta(0, 62, 852000), 44.275]
    """
    elements=fline.split()

    # Basic consistency check
    # second condition for len > 2 prevents an index error in the next one
    if len(elements) != 7 or (len(elements)>2 and elements[2]!="-"):
        return [None,'','',0,timedelta(0),0.0]
    return [
        datetime.strptime(Pilot.nowPrefix+" " + elements[0],'%Y-%m-%d %H:%M:%S.%f'),
        elements[1],
        elements[3],
        int(elements[4]),
        timedelta(minutes = int(elements[5].split(":")[0]), seconds = float(elements[5].split(":")[1])),
        float(elements[6].split(",")[0] + "." + elements[6].split(",")[1])
    ];
"""
    6 output fields:
    0 - time of lap, None if line is invalid
    1 - code
    2 - name
    3 - lap number
    4 - time of lap, MM:SS.FFF
    5 - average speed, float with commas
"""


def parse_date(datestring):
    return datetime.strptime(Pilot.nowPrefix+' '+datestring,"%Y-%m-%d %H:%M:%S.%f")

def kartparser():
    """
    Main program: parse an user-provided log file
    >>> sys.argv=['kartparser']; kartparser()
    Usage: python3 kartparser <logfile>
    2
    >>> sys.argv=['kartparser','/dev/nothing']; kartparser()
    Error reading file /dev/nothing, please check
    Error message:  [Errno 2] No such file or directory: '/dev/nothing'
    3
    """

    if len(sys.argv) != 2:
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
    f.readline()

    # main loop for gobbling up data and setting up pilots
    fline=""
    for fline in f.readlines():
        elements=parse_line(fline)
        if elements[0] is None:
            print(f'Invalid line: ' + fline)
        else:
            pilot=Pilot.get_pilot(elements[1], elements[2]) # code, name
            if pilot is None:
                pilot=Pilot(elements[1], elements[2]) # New pilot, code, name
            pilot.add_lap(elements[0], elements[3],
                elements[4], elements[5])

    # finished race. Let's update positions, best lap time, total race duration.
    Pilot.update_finished()

    print(f'Posição\tHora de chegada\t\tCódigo\tNome\t\t\tVoltas\tMelhor Volta\tVelocidade Média Total\tTempo Total')
    for pilot in Pilot.all_pilots():
        print( (str(pilot.position) if pilot.finished else "-") + "\t" + \
            datetime.strftime(pilot.end_time,'%H:%M:%S.%f')[0:12] + \
            '\t\t' + pilot.code + '\t' + \ pilot.name.ljust(20) + '\t' + str(pilot.max_lap) + \
            '\t' + str(pilot.best_lap_time)[2:10] + '\t' + "{:.2f}".format(pilot.average_speed) + \
            '\t\t\t' + str(pilot.total_time)[2:10])
    print(f'\n\nEstatísticas:\n')
    print(f'Melhor tempo de volta: ' + str(Pilot.best_lap())[2:10])
    print(f'Tempo total da corrida: ' + str(Pilot.total_time())[2:10])

    return 0


if __name__ == "__main__":
    sys.exit(kartparser())
