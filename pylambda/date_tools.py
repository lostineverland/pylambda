import datetime

ISO_8601_SECONDS = '%Y-%m-%dT%H:%M:%S'
ISO_8601_MINUTES = '%Y-%m-%dT%H:%M'
ISO_8601_HOURS = '%Y-%m-%dT%H'
ISO_8601_DAYS = '%Y-%m-%d'
ISO_8601_MONTHS = '%Y-%m'
ISO_8601_YEARS = '%Y'


def datetime_to_ISO_second(dt):
    return dt.strftime(ISO_8601_SECONDS)

def datetime_to_ISO_minute(dt):
    return dt.strftime(ISO_8601_MINUTES)

def datetime_to_ISO_hour(dt):
    return dt.strftime(ISO_8601_HOURS)

def datetime_to_ISO_day(dt):
    return dt.strftime(ISO_8601_DAYS)

def datetime_to_ISO_month(dt):
    return dt.strftime(ISO_8601_MONTHS)

def datetime_to_ISO_year(dt):
    return dt.strftime(ISO_8601_YEARS)
