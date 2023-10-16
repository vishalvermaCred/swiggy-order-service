from typing import Optional

from app.database import Postgres


class AppContext:
    db: Optional[Postgres]
    producer: Optional[None]


app_context = AppContext()
