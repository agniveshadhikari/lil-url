from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    username: str
    first_name: str
    middle_name: str
    last_name: str
    access_level: str
    last_login_time: datetime
