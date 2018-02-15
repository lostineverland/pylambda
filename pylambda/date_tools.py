import datetime
from dateutil.relativedelta import relativedelta
from utils import comp
import objtypes

# ISO_8601 string formats
iso_8601 = objtypes.objDict(
    MICROSECONDS='%Y-%m-%dT%H:%M:%S.%f',
    SECONDS='%Y-%m-%dT%H:%M:%S',
    MINUTES='%Y-%m-%dT%H:%M',
    HOURS='%Y-%m-%dT%H',
    DAYS='%Y-%m-%d',
    MONTHS='%Y-%m',
    YEARS='%Y',
)

granularity_by_len = {
    26: 'MICROSECONDS',
    19: 'SECONDS',
    16: 'MINUTES',
    13: 'HOURS',
    10: 'DAYS',
    7: 'MONTHS',
    4: 'YEARS',
}

def get_iso_format(iso_dt):
    return iso_8601[granularity_by_len.get(len(iso_dt), 'MICROSECONDS')]

class fromIsoToIso(object):
    """a set of functions which take an ISO_8601 time string
    and return an ISO_8601 time string
    """
    @staticmethod
    def add(value, iso_dt, unit=None, granularity=None):
        unit = unit or granularity_by_len[len(iso_dt)].lower()
        granularity = granularity or granularity_by_len[len(iso_dt)].lower()
        return comp(
            fromIsoToDt.to_dt,
            [getattr(fromDtToDt, 'add_{}'.format(unit)), value],
            getattr(fromDtToIso, 'to_{}'.format(granularity))
        )(iso_dt)

    @staticmethod
    def subtract(value, iso_dt, unit=None, granularity=None):
        unit = unit or granularity_by_len[len(iso_dt)].lower()
        granularity = granularity or granularity_by_len[len(iso_dt)].lower()
        return comp(
            fromIsoToDt.to_dt,
            [getattr(fromDtToDt, 'subtract_{}'.format(unit)), value],
            getattr(fromDtToIso, 'to_{}'.format(granularity))
        )(iso_dt)

class fromDtToDt(object):
    """a set of functions which take a datetime object
    and return a datetime object
    """
    @staticmethod
    def subtract_microseconds(microseconds, dt):
        delta = datetime.timedelta(microseconds=microseconds)
        return dt - delta
        
    @staticmethod
    def add_microseconds(microseconds, dt):
        delta = datetime.timedelta(microseconds=microseconds)
        return dt + delta
        
    @staticmethod
    def subtract_seconds(seconds, dt):
        delta = datetime.timedelta(seconds=seconds)
        return dt - delta
        
    @staticmethod
    def add_seconds(seconds, dt):
        delta = datetime.timedelta(seconds=seconds)
        return dt + delta
        
    @staticmethod
    def subtract_minutes(minutes, dt):
        delta = datetime.timedelta(seconds=60*minutes)
        return dt - delta
        
    @staticmethod
    def add_minutes(minutes, dt):
        delta = datetime.timedelta(seconds=60*minutes)
        return dt + delta
        
    @staticmethod
    def subtract_hours(hours, dt):
        delta = datetime.timedelta(seconds=3600*hours)
        return dt - delta
        
    @staticmethod
    def add_hours(hours, dt):
        delta = datetime.timedelta(seconds=3600*hours)
        return dt + delta
        
    @staticmethod
    def subtract_days(days, dt):
        delta = datetime.timedelta(days=days)
        return dt - delta
        
    @staticmethod
    def add_days(days, dt):
        delta = datetime.timedelta(days=days)
        return dt + delta
        
    @staticmethod
    def subtract_months(months, dt):
        delta = relativedelta(months=months)
        return dt - delta
        
    @staticmethod
    def add_months(months, dt):
        delta = relativedelta(months=months)
        return dt + delta
        
    @staticmethod
    def subtract_years(years, dt):
        delta = relativedelta(years=years)
        return dt - delta
        
    @staticmethod
    def add_years(years, dt):
        delta = relativedelta(years=years)
        return dt + delta
        
class fromIsoToDt(object):
    """a set of functions which take an ISO_8601 time string
    and return a datetime object
    """
    @staticmethod
    def to_dt(iso_dt):
        return datetime.datetime.strptime(iso_dt, get_iso_format(iso_dt))

    @staticmethod
    def from_microsecond(iso_dt):
        return datetime.datetime.strptime(iso_dt, iso_8601.MICROSECONDS)

    @staticmethod
    def from_second(iso_dt):
        return datetime.datetime.strptime(iso_dt, iso_8601.SECONDS)

    @staticmethod
    def from_minute(iso_dt):
        return datetime.datetime.strptime(iso_dt, iso_8601.MINUTES)

    @staticmethod
    def from_hour(iso_dt):
        return datetime.datetime.strptime(iso_dt, iso_8601.HOURS)

    @staticmethod
    def from_day(iso_dt):
        return datetime.datetime.strptime(iso_dt, iso_8601.DAYS)

    @staticmethod
    def from_month(iso_dt):
        return datetime.datetime.strptime(iso_dt, iso_8601.MONTHS)

    @staticmethod
    def from_year(iso_dt):
        return datetime.datetime.strptime(iso_dt, iso_8601.YEARS)

class fromDtToIso(object):
    """a set of functions which take a datetime object
    and return an ISO_8601 time string
    """
    @staticmethod
    def to_microseconds(dt):
        return dt.strftime(iso_8601.MICROSECONDS)

    @staticmethod
    def to_seconds(dt):
        return dt.strftime(iso_8601.SECONDS)

    @staticmethod
    def to_minutes(dt):
        return dt.strftime(iso_8601.MINUTES)

    @staticmethod
    def to_hours(dt):
        return dt.strftime(iso_8601.HOURS)

    @staticmethod
    def to_days(dt):
        return dt.strftime(iso_8601.DAYS)

    @staticmethod
    def to_months(dt):
        return dt.strftime(iso_8601.MONTHS)

    @staticmethod
    def to_years(dt):
        return dt.strftime(iso_8601.YEARS)
