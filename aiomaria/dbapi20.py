import sys, datetime, time
sys.dont_write_bytecode = True

from mariadb.dbapi20 import (
    BINARY, STRING, NUMBER, DATE, TIME, DATETIME, ROWID,
    apilevel, paramstyle, threadsafety
)

async def Binary(object) -> bytes:
    """Constructs an object capable of holding a binary value."""
    return bytes(object)

async def Date(year: int, month: int, day: int) -> datetime.date:
    """Constructs an object holding a date value."""
    return datetime.date(year, month, day)

async def Time(hour: int, minute: int, second: int) -> datetime.time:
    """Constructs an object holding a time value."""
    return datetime.time(hour, minute, second)

async def Timestamp(year: int, month: int, day: int, hour: int, minute: int, second: int) -> datetime.datetime:
    """Constructs an object holding a datetime value."""
    return datetime.datetime(year, month, day, hour, minute, second)

async def DateFromTicks(ticks: int) -> datetime.date:
    """Constructs an object holding a date value from the given ticks value (number of seconds since the epoch)."""
    return await Date(*time.localtime(ticks)[:3])

async def TimeFromTicks(ticks: int) -> datetime.time:
    """Constructs an object holding a time value from the given ticks value (number of seconds since the epoch)."""
    return await Time(*time.localtime(ticks)[3:6])

async def TimestampFromTicks(ticks: int) -> datetime.datetime:
    """Constructs an object holding a datetime value from the given ticks value (number of seconds since the epoch)."""
    return datetime.datetime(*time.localtime(ticks)[:6])
