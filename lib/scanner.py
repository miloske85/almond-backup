
import os
import logging
import sys
import time

from subprocess import check_output
from datetime import datetime
from calendar import monthcalendar

from lib.controller import Controller


class Scan(Controller):

    archives = []
    archives_dict = []

    path = ''
    retention = 1000000

    def __init__(self, config):
        super().__init__(config)
        logging.basicConfig(filename=self.logfile, level=logging.INFO)

    def scan_archives(self, path, action, retention=100000):
        self.retention = retention * 86400

        # these have to be reset
        self.archives_dict = []
        self.archives = []

        try:
            files = [f.path for f in os.scandir(path) if f.is_file()]

            for file in files:
                archive = {}
                archive['file'] = file

                if self.age_by == 'timestamp':
                    archive['timestamp'] = self.get_timestamp(file)
                elif self.age_by == 'filename':
                    archive['timestamp'] = self.get_ts_from_filename(file)
                else:
                    logging.error(str(datetime.now()) + " Wrong age_by parameter")
                    print('Wrong age_by parameter')
                    sys.exit(1) #TODO - validate config file at the start

                self.archives_dict.append(archive)

        except IOError as error:
            logging.error(str(datetime.now()) + " Scanner IO Error: " + str(error))

        if action == 'purge':
            self.process_purge()
        elif action == 'lc_weekly':
            self.process_weekly()
        elif action == 'lc_monthly':
            self.process_monthly()
        elif action == 'lc_quarterly':
            self.process_quarterly()
        elif action == 'lc_yearly':
            self.process_yearly()
        else:
            logging.error(str(datetime.now()) + " Wrong action parameter: " + action)

    def get_timestamp(self, file):
        return os.path.getmtime(file)
    def get_ts_from_filename(self, file):
        filedate = file.split('_')[-1]
        ts = filedate.split('.')[0]  # filename must be in format - x1_x2_2022-12-17.tar.bz2.gpg.whatever
        return time.mktime(datetime.strptime(ts, "%Y-%m-%d").timetuple())

    def process_purge(self):
        if self.age_by == 'filename':
            self.retention += 1

        now = int(time.time())
        for archive in self.archives_dict:
            if now - archive['timestamp'] > self.retention:
                self.archives.append(archive['file'])
    def process_weekly(self):
        for archive in self.archives_dict:
            dt = datetime.fromtimestamp(archive['timestamp'])
            if dt.weekday() == self.day_weekly:
                self.archives.append(archive['file'])

    def process_monthly(self):
        for archive in self.archives_dict:
            dt = datetime.fromtimestamp(archive['timestamp'])
            month = monthcalendar(dt.year, dt.month)
            # check if the last week has the day
            if month[-1][self.day_weekly]:
                last_day = month[-1][self.day_weekly]
            # else check the second last week
            else:
                last_day = month[-2][self.day_weekly]

            if dt.day == last_day:
                self.archives.append(archive['file'])

    def process_quarterly(self):
        for archive in self.archives_dict:
            dt = datetime.fromtimestamp(archive['timestamp'])
            month = dt.month

            if month in self.months_quarterly:
                self.archives.append(archive['file'])

    def process_yearly(self):
        for archive in self.archives_dict:
            dt = datetime.fromtimestamp(archive['timestamp'])
            month = dt.month

            if month == self.month_yearly:
                self.archives.append(archive['file'])
    def get_archives(self):
        return self.archives


