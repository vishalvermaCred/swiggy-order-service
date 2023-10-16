from typing import Optional

from app.database import Postgres

"""
    file to store the context of app
"""


class AppContext:
    db: Optional[Postgres]
    producer: Optional[None]


app_context = AppContext()
