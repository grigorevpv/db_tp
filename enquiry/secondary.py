import pytz


def convert_time(created):
    if created is None:
        return 'Null'
    zone = pytz.timezone('Europe/Moscow')
    if created.tzinfo is None:
        created = zone.localize(created)
    utc_time = created.astimezone(pytz.utc)
    utc_str = utc_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
    utc_str = utc_str[:-3] + 'Z'
    return utc_str

def queries(cursor, query_body, params, field=None):
    try:
        cursor.execute(query_body, params)

        if field is None:

            return cursor
        cursor.fetchone()[field]
    except:
        print("[queries] execute error")
        raise Exception('execute exception')