# gdrivebackup
Backup scripts that work in conjunction with overGrive to perform Google Drive backups on a Raspberry Pi.

## Overview

See [this blog post](http://blog.mattwoodward.com/2017/11/how-to-back-up-google-drive-to.html) for full details.

Basically this is two scripts:
* syncfiles.py -- syncs one directory to another
* archive.py -- archives a directory to a TGZ

How I'm using them:
* [overGrive](https://www.thefanclub.co.za/overgrive) syncs Google Drive to a Raspberry Pi
* syncfiles.py runs hourly to copy the Google Drive files to another directory on the Raspberry Pi
* arhive.py runs nightly to retain a TGZ of the Google Drive backup
* Notifications on script activity are sent using [Pushover](https://pushover.net)

## Configuration and Usage

* Create a .env file in the root that has values for the settings outlined in the .envsample file
* Create a virtualenv for the project
* `pip install -r requirements.txt`
* Run the scripts manually, or configure to run via cron

## Caveats

* The sync script does a purge of the target directory, i.e. files that exist in target and not in source will be deleted when the sync runs

## Future Ideas

* Eliminate the dependency on overGrive and use the Google Drive API directly (though for the purposes of this project $5 was a cheap way to save quite a bit of time)
