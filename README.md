DoTheBackup
===========

a little python script for handling my backups. if `type: month` its using hardlinks between days to save diskspace.

## usage
	Usage:
		DoTheBackup.py (-f <config> | --file <config>)

	Options:
		-f --file        Reads config from YAML File

## config
	# destination where the logs will be
	log_dir: /var/log/DoTheBackup
	# define your backups here
	backup:
		my_documents:
			# "month" means that it will save the backup in daily directories
			# for example: "/media/backup/documents/07"
			type: month
			source: /home/user/documents
			destination: /media/backup/documents
			# rsync --exclude patterns here
			exclude:
				- foo
				- bar
			# rsync --include patterns here
			include:
				- very_important_dir
		video:
			# "once" backups straight in the destination directory
			# for example: "/media/backup/Videos"
			type: once
			source: /home/user/Media/Videos
			destination: /media/backup/Videos

## install
for example in /opt

1. `cd /opt`
2. `git clone https://github.com/xsteadfastx/DoTheBackup.git`
3. `cd DoTheBackup`
4. `virtualenv venv`
5. `source venv/bin/activate`
6. `pip install -r requirements.txt`
7. `cp DoTheBackup.yaml.dist DoTheBackup.yaml`
8. `vim DoTheBackup.yaml`

## running in crontab
i use a shell wrapper script for handling the virtualenv

1. `/opt/DoTheBackup`
2. `cp DoTheBackup-cron.sh.dist DoTheBackup-cron.sh`
3. `vim DoTheBackup-cron.sh`
4. edit your crontab and add `/opt/DoTheBackup/DoTheBackup-cron.sh`
