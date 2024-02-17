from datetime import datetime, time
from pytz import timezone

tz = timezone('Europe/Moscow')

def get_date() -> datetime:
    return datetime.now(tz)

def get_time() -> time:
    return get_date().time()

def get_weekday() -> int: # 0 - Monday, 6 - Sunday
    return get_date().weekday()

def get_time_to(when: time) -> int:
    now = get_time()

    delta_hours = when.hour - now.hour
    delta_minutes = when.minute - now.minute
    delta_seconds = when.second - now.second

    if when < now:
        delta_hours += 24

    return delta_hours * 3600 + delta_minutes * 60 + delta_seconds

def time_from_values(hours: int, minutes: int = 0, seconds: int = 0) -> time:
    return time(hours, minutes, seconds)

def time_from_value(value: int) -> time:
    return time_from_values(value // 3600, (value % 3600) // 60, value % 60)

def time_to_values(t: time) -> int:
    return t.hour * 3600 + t.minute * 60 + t.second

def add_time(t: time, value: int) -> time:
    return time_from_value(time_to_values(t) + value)

def is_time_between(start: time, end: time, now: time) -> bool:
    if start <= end:
        return start <= now <= end
    else:
        return start <= now or now <= end

def make_readable_date(date: datetime) -> str:
    return date.strftime('%d.%m.%Y %H:%M:%S')

def make_readable_time(t: time) -> str:
    return t.strftime('%H:%M')
