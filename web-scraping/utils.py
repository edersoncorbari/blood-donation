import re
import datetime
import pytz
import datetime


def dt_utc_format(dt):
    tz = datetime.datetime.strftime(dt, '%Y-%m-%dT%H:%M:%S.%f')
    return tz[:-3] + 'Z'


def tz_to_utc(dt):
    local = pytz.timezone('UTC')
    local_dt = local.localize(dt, is_dst=None)
    return local_dt.astimezone(pytz.utc)


def iso_dt_format(dt):
    dtiso = re.findall(r'[0-9]+', dt)
    dtstr = (
        dtiso[2] +
        "-" +
        dtiso[1] +
        "-" +
        dtiso[0] +
        " " +
        dtiso[3] +
        ":" +
        dtiso[4] +
        ":00")
    return dtstr
