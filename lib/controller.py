
import sys
class Controller:

    config = {}

    logfile = ''
    archive_base_path = ''
    items = []

    scanner = None
    purge = None
    archives = []

    move_dry_run = False
    create_dry_run = False
    delete_dry_run = False
    mkdir = False
    age_by = ''
    day_weekly = ''
    months_quarterly = []
    month_yearly = 12

    def __init__(self, config):
        self.config = config

        self.logfile = config['global']['logfile']
        self.archive_base_path = config['global']['archive_base_path']

        if 'archive_tmp_path' in config['global']:
            self.archive_tmp_path = config['global']['archive_tmp_path']

        self.items = config['items']

        if 'create_dry_run' in config['global']:
            self.create_dry_run = config['global']['create_dry_run']

        if 'move_dry_run' in config['global']:
            self.move_dry_run = config['global']['move_dry_run']

        if 'delete_dry_run' in config['global']:
            self.delete_dry_run = config['global']['delete_dry_run']

        if 'mkdir' in config['global']:
            self.mkdir = config['global']['mkdir']

        self.age_by = config['global']['age_by']

        day_weekly = config['global']['day_weekly'].lower()

        if day_weekly == 'monday':
            self.day_weekly = 0
        elif day_weekly == 'tuesday':
            self.day_weekly = 1
        elif day_weekly == 'wednesday':
            self.day_weekly = 2
        elif day_weekly == 'thursday':
            self.day_weekly = 3
        elif day_weekly == 'friday':
            self.day_weekly = 4
        elif day_weekly == 'saturday':
            self.day_weekly = 5
        elif day_weekly == 'sunday':
            self.day_weekly = 6
        else:
            print('Wrong day_weekly')
            sys.exit(1)

        self.months_quarterly = config['global']['months_quarterly']
        self.month_yearly = config['global']['month_yearly']

        if self.month_yearly not in self.months_quarterly:
            print('Yearly month is not in the given quarterly months')
            sys.exit(1)

    def debug(self):
        pass
