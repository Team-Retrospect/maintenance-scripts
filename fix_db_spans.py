#!/bin/python3

from cassandra.cluster import Cluster
from cassandra.query import dict_factory
import json

API_CLUSTER = ['cassandra.xadi.io']
KEYSPACE = 'retrospect'

QUERY_DB_SPANS = "SELECT JSON * FROM db_span_buffer;"
QUERY_FIND_ACTUAL_VALUES = "\
SELECT session_id, user_id, chapter_id, trigger_route \
FROM spans \
WHERE trace_id='{0}' \
LIMIT 1;"
QUERY_INSERT_NEW = "INSERT INTO spans JSON '{0}';"
QUERY_DELETE = "DELETE FROM db_span_buffer WHERE span_id='{0}';"

def get_db_spans(session):
    rows = session.execute(QUERY_DB_SPANS)
    db_spans = {}
    for j in rows :
        values = json.loads(j['[json]'])
        span_id = values['span_id']
        print("Processing span id", span_id)
        db_spans[span_id] = values
        # find correct session_id, user_id, chapter_id, trigger_route
        query = QUERY_FIND_ACTUAL_VALUES.format(values['trace_id'])
        actual = session.execute(query).one()

        if actual is None :
            print("-> no actual values found: skipping!")
            continue

        # update values
        values['session_id'] = actual['session_id']
        values['user_id'] = actual['user_id']
        values['chapter_id'] = actual['chapter_id']
        values['trigger_route'] = actual['trigger_route']

        if values['trigger_route'] == "" :
            continue

        # insert into spans
        query = QUERY_INSERT_NEW.format(json.dumps(values))
        session.execute(query)
        # print(query)

        # delete from buffer
        query = QUERY_DELETE.format(span_id)
        session.execute(query)
        # print(query)
        print("Done!")

if __name__ == "__main__":
    cluster = Cluster(API_CLUSTER,port=9042)
    session = cluster.connect(KEYSPACE, wait_for_all_pools=True)
    session.execute(f'USE {KEYSPACE};')
    session.row_factory = dict_factory

    get_db_spans(session)
