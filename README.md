# Almond Backup

Having a backup copy of your files, on a RAID array, or cloud (if you're a normie) is important, but often not enough. For important files it is highly desirable to have multiple backup copies.

Almond Backup can:

- create daily, optionally encrypted, `tar.bz2` archives (optionally excluding some files/folder)
- manage lifecycle of backup archives (daily, weekly, monthly, quarterly and yearly)

These actions are independent, you can create archives without managing lifecycle, or just manage lifecycle. This is controlled by config file (see below).

It is designed to run on a Linux/Unix system, using `subprocess.call()` to interact with the system. Tested on Linux. I don't know if it would work on a mac and I'm not interested in providing support for macs.

## Usage

`almond-bkp [-h] [-v] [-c CONFIG_FILE] [-y YAML_CONFIG_FILE] [--check] [--debug]`

  `-h, --help            show this help message and exit`

  `-v, --version         Print version info`

  `-c CONFIG_FILE, --config-file JSON CONFIG_FILE`

  `-y YAML_CONFIG_FILE, --yaml-config-file YAML_CONFIG_FILE`

  `--check               Validate config file`

  `--debug               Print debug info`


For each item given in the configuration file, a folder will be created, with the same name as `name` parameter. Inside this folder subfolders will be created for each item in `lifecycle` section. New archives are added to `daily` folder with the name in the following format:

`hostname_name_YYYY-MM-DD.tar.bz2[.gpg]`

The order of operation is:

- move
- purge
- create

That is, first archives that match conditions are moved up the lifecycle (daily-to-weekly, weekly-to-monthly, etc.). Then old archives are deleted. And finally, new archives are created.
Archives don't have to have full lifecycle, but lifecycle must be contiguous. If you don't want to keep quartely and yearly archive, simply omit these entries from config file, but don't omit quarterly if you want to have yearly archives.

Monthly archives are created on the last `day_weekly` in a given month.

## Config files

Default config file format is `JSON`, because Python natively supports it. Optionally `YAML` can be used if `pyyaml` is installed, or a `YAML` config file can be converted to `JSON` on a system that has `pyyaml` installed (use `scipts/config_parser.py` for this).

Default config file location, used if config file is not supplied as an argument is: `/usr/local/etc/almond.json`

### Config file reference

See `config/sample.yml`

Some parameters need further explanation:

`age_by` sets how the age of an archive will be determined. `timestamp` will use Python's `os.path.getmtime()` to get the timestamp and `filename` will get the age from the filename. Since filename contains only the date, timestamp would be equal to that date on midnight. This is undesirable, since it would cause those archives to appear older, so a day is added to the timestamp if `filename` method is chosen.

The main advantages of `filename` method are that you can run this script at different times of day and still get consistent results and you do no depend on file timestamps which might change for various reasons.

`archive_tmp_path` is important because TAR first creates archives to this location and then encrypts them if `key` is specified. This is useful if you are backing up to an unencrypted removable drive, for example.

### Partial operation

#### Only create archives

If you want to only create archives (in `daily` folder), simply omit the `lifecycle` section entirely from config file.

#### Only manage lifecycle

If you want to only manage lifecycle, omit `source` location form config file. This is useful if for example you are uploading archives daily to a remote server or removable storage where you have lots of space and want to keep more archives than on the machine where you create backup archives. 
