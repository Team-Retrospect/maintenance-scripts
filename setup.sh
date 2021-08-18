#!/bin/sh

apt update
apt install python3 python3-pip
pip3 install cassandra-driver yaml

(crontab -l 2>/dev/null; echo "* * * * * python3 cleaner/fix_db_spans.py") | crontab -
(crontab -l 2>/dev/null; echo "* * 0 * * python3 cleaner/cleanup.py") | crontab -
