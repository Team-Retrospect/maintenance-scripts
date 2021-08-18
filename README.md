# Retrospect DB maintenance scripts

There are 2 maintenance scripts and a yaml file. Setup:

- Install the requirements
- Make sure the yaml file is in the same folder as the python scripts
- Update the yaml file
- Add to crontab

## Requirements:

Run these to install Python (which needs superuser privilegesif not already installed), and then install the cassandra-driver and pyyaml packages.

```sh
apt-get install python3
pip install cassandra-driver pyyaml
```

## Update the yaml file

Update the cluster with the URL names or IP addresses of your Retrospect Cassandra instances.

Also, if you wish to retain trace/span data for more or less than a week, change that numer, too.

```yml
cluster:
  - "some.ip.goes.here"

retention_days: 7
```

## Add to crontab

Add the files to the crontab. the suggested settings are:

```
* * * * * python3 cleaner/fix_db_spans.py   # fix db spans every minute
* * 0 * * python3 cleaner/cleanup.py        # purge old data every day
```

