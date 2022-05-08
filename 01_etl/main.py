from datetime import datetime

from config import DSL, DSL_ELK, INDEX_MOVIES
from elk_saver import ELKConnections
from pg_loader import PGLoader
from utility import get_or_set_stage, get_sql

if __name__ == '__main__':
    start_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    date_time = get_or_set_stage()
    sql = get_sql(date_time)
    data = PGLoader(DSL).make_request(sql)
    ELKConnections(credentials=DSL_ELK, index=INDEX_MOVIES).bulk_update(data)
    get_or_set_stage(start_time)
