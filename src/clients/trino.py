import pytz
from trino.dbapi import connect
from trino.auth import BasicAuthentication
from src.config import (
    TRINO_HOST,
    TRINO_PORT,
    TRINO_SCHEME,
    TRINO_USERNAME,
    TRINO_PASSWORD,
)

timezone = pytz.timezone("UTC")

# client = connect(
#     host=TRINO_HOST,
#     port=TRINO_PORT,
#     http_scheme=TRINO_SCHEME,
#     auth=BasicAuthentication(TRINO_USERNAME, TRINO_PASSWORD),
# )
client = connect(
    host="trino.mescobrad.digital-enabler.eng.it",
    port=443,
    http_scheme="https",
    auth=BasicAuthentication("mescobrad-dwh-user", "dwhouse"),
    timezone=str(timezone),
)
