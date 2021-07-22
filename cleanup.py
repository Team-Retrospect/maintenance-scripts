#!/bin/python

from cassandra.cluster import Cluster
from datetime import datetime, timedelta

API_CLUSTER = ['cassandra.xadi.io']
KEYSPACE = 'project'
DAYS_TO_RETAIN = 1

CUTOFF = (datetime.now() - timedelta(days = DAYS_TO_RETAIN)).timestamp()

BATCH_STATEMENT = """\
BEGIN BATCH
{0}
APPLY BATCH;\
"""
DELETE_STATEMENT = """
DELETE FROM spans       WHERE session_id = '{0}';
DELETE FROM events      WHERE session_id = '{0}';
DELETE FROM snapshots   WHERE session_id = '{0}';
"""

def cleanse_spans(session):
    ids = {}
    rows = session.execute('SELECT session_id, time_sent FROM spans;')
    counter = 0
    for row in rows:
        delta = (row.time_sent / 10**6)
        if CUTOFF > (row.time_sent / 10**6) :
            ids[row.session_id] = True
        counter += 1

    commands = "".join([DELETE_STATEMENT.format(i) for i in ids])
    batch = BATCH_STATEMENT.format(commands)

    print(batch)
    # session.execute(batch)

if __name__ == "__main__":
    cluster = Cluster(API_CLUSTER,port=9042)
    session = cluster.connect(KEYSPACE, wait_for_all_pools=True)
    session.execute(f'USE {KEYSPACE};')

    cleanse_spans(session)
