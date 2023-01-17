
import os
import sys
import logging

import subprocess
from datetime import datetime

from lib.controller import Controller
from lib.scanner import Scan


class Purge(Controller):

    scanner = None

    def __init__(self, config):
        super().__init__(config)
        logging.basicConfig(filename=self.logfile, level=logging.INFO)
        self.scanner = Scan(config)

        self.purge_item('daily')
        self.purge_item('weekly')
        self.purge_item('monthly')
        self.purge_item('quarterly')
        self.purge_item('yearly')

    def purge_item(self, bkp_class):
        # logging.info(str(datetime.now()) + ' Starting to purge archives ' + str(bkp_class))

        if bkp_class == 'daily':
            multiplier = 1
        elif bkp_class == 'weekly':
            multiplier = 7
        elif bkp_class == 'monthly':
            multiplier = 30
        elif bkp_class == 'quarterly':
            multiplier = 90
        elif bkp_class == 'yearly':
            multiplier = 365
        else:
            logging.error(str(datetime.now()) + " Wrong bkp_class: ")
            sys.exit(1)

        for item in self.items:
            if bkp_class not in item['lifecycle']:
                # logging.info(str(datetime.now()) + ' Lifecycle not defined: ' + str(bkp_class) + ', skipping')
                continue

            path = self.archive_base_path + '/' + item['name'] + '/' + bkp_class
            try:
                retention = int(item['lifecycle'][bkp_class]) * multiplier
            except:
                logging.warn(str(datetime.now()) + " Lifecycle not defined for: " + str(path))

            if os.access(path, os.W_OK) and retention > 0:
                self.scanner.scan_archives(path, 'purge', retention)
                file_list = self.scanner.get_archives()

                if len(file_list) == 0:
                    logging.info(str(datetime.now()) + " No archives found for: " + str(item['name']) + ' / ' + bkp_class)

                for f in file_list:
                    logging.info(str(datetime.now()) + " Deleting archive: " + f)
                    if not self.delete_dry_run:
                        subprocess.call(['rm', '-f', f])
                    else:
                        logging.info("Not deleting, dry run")
            else:
                logging.error(str(datetime.now()) + " Location not writable: " + str(path))