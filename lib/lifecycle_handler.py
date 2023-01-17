
import logging
import subprocess
import os
import sys

from datetime import datetime

from lib.controller import Controller
from lib.scanner import Scan

class LifecycleHandler(Controller):

    def __init__(self, config):
        super().__init__(config)
        logging.basicConfig(filename=self.logfile, level=logging.INFO)
        self.scanner = Scan(config)

        self.process_archives()

    def process_archives(self):
        for item in self.items:
            if 'lifecycle' in item:
                if 'weekly' in item['lifecycle']:
                    self.move_to_weekly(item['name'])
                if 'monthly' in item['lifecycle']:
                    self.move_to_monthly(item['name'])
                if 'quarterly' in item['lifecycle']:
                    self.move_to_quarterly(item['name'])
                if 'yearly' in item['lifecycle']:
                    self.move_to_yearly(item['name'])
            else:
                logging.info(str(datetime.now()) + ' ' + item['name'] + ' has no lifecycle.')

    def move_to_weekly(self, name):
        self.move_to_another_class(name, 'daily', 'weekly')

    def move_to_monthly(self, name):
        self.move_to_another_class(name, 'weekly', 'monthly')

    def move_to_quarterly(self, name):
        self.move_to_another_class(name, 'monthly', 'quarterly')

    def move_to_yearly(self, name):
        self.move_to_another_class(name, 'quarterly', 'yearly')

    def move_to_another_class(self, name, source, destination):
        lifecycle = 'lc_' + str(destination)
        source_path = self.archive_base_path + '/' + name + '/' + str(source)
        destination_path = self.archive_base_path + '/' + name + '/' + str(destination)

        if self.mkdir:
            if not os.path.isdir(destination_path):
                logging.info(str(datetime.now()) + " Creating directory: " + str(destination_path))
                subprocess.call(['mkdir', '-p', destination_path])
            if not os.path.isdir(source_path):
                logging.info(str(datetime.now()) + " Creating directory: " + str(source_path))
                subprocess.call(['mkdir', '-p', source_path])

        self.scanner.scan_archives(source_path, lifecycle)
        archives = self.scanner.get_archives()

        if os.access(destination_path, os.W_OK):
            for archive in archives:
                logging.info(str(datetime.now()) + " Moving: " + str(archive) + ' to ' + str(destination) + ' folder')
                if not self.move_dry_run:
                    subprocess.call(['mv', archive, destination_path])
                else:
                    logging.info("Not moving, dry run")
        else:
            logging.error(str(datetime.now()) + " Location not writable: " + str(destination_path))

