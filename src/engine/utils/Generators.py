from uuid import uuid4
from datetime import datetime, timezone


def getId() -> str:
    return str(uuid4())


def getDateTimeNow() -> str:
    return str(datetime.now(tz=timezone.utc))
