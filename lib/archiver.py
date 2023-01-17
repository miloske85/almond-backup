
import logging
import subprocess
import os
import sys

from datetime import datetime

from lib.controller import Controller

class Archive(Controller):


    def __init__(self, config):
        super().__init__(config)
        logging.basicConfig(filename=self.logfile, level=logging.INFO)
        self.process_backup()

    def process_backup(self):
        for item in self.items:
            if 'source' in item:
                self.create_archive(item)
            else:
                logging.info(str(datetime.now()) + ' ' + item['name'] + ' has no source, not creating an archive')

    def create_archive(self, item):
        now_time = datetime.now()
        now = now_time.strftime('%Y-%m-%d')
        hostname = str(subprocess.check_output(['hostname']).decode()).split('.')[0].strip()
        archive_name = self.archive_tmp_path + "/" + hostname + '_' + item['name'] + "_" + now + ".tar.bz2"

        if not os.access(self.archive_tmp_path, os.W_OK):
            logging.error(str(datetime.now()) + ' Temporary archive location not writable')
            print('ERROR: Temporary archive location not writable')
            sys.exit(2)

        if 'exclude_file' in item:
            # pass tar exclude file
            if os.access(item['source'], os.R_OK):
                logging.info(str(datetime.now()) + ' Creating daily archive with exclusion for: ' + str(item['name']))
                if not self.create_dry_run:
                    subprocess.call(['tar', '--exclude-from=' + item['exclude_file'], '-cjf', archive_name, item['source']])
                    self.finalize_archive(item, archive_name)
                else:
                    logging.info("Not creating, dry run")
            else:
                logging.error(str(datetime.now()) + ' Source not readable for: ' + str(item['name']))
        else:
            if os.access(item['source'], os.R_OK):
                logging.info(str(datetime.now()) + ' Creating daily archive for: ' + str(item['name']))
                if not self.create_dry_run:
                    subprocess.call(['tar', '-cjf', archive_name, item['source']])
                    self.finalize_archive(item, archive_name)
                else:
                    logging.info("Not creating, dry run")
            else:
                logging.error(str(datetime.now()) + ' Source not readable for: ' + str(item['name']))

    def finalize_archive(self, item, archive_name):
        destination = self.archive_base_path + '/' + item['name'] + '/' + 'daily'
        if 'key' in item:
            if not os.access(item['key'], os.R_OK):
                logging.error(str(datetime.now()) + ' Encryption key not readable for: ' + item['name'])
                logging.info(str(datetime.now()) + ' Removing temporary archive for: ' + str(item['name']))
                subprocess.call(['rm', '-f', archive_name])
                return 1

            logging.info(str(datetime.now()) + ' Encrypting archive ' + str(item['name']))
            subprocess.call(['gpg', '-c', '--cipher-algo=AES256', '--batch', '--passphrase-file', item['key'], archive_name])
            subprocess.call(['rm', '-f', archive_name])
            subprocess.call(['mv', archive_name + '.gpg', destination])
        else:
            subprocess.call(['mv', archive_name, destination])

