from datetime import datetime
from pydantic import BaseModel


class Point(BaseModel):
    # how many points this represents
    points: int
    # The date the points were added
    date: datetime

    def __init__(self, points: int, date_str: str):

        dt = datetime.strptime(date_str, '%m/%d %I%p')
        dt.replace(year=datetime.now().year)  # Assume we are always adding points from the current year

        data = {
            'points': points,
            'date': dt
        }
        super().__init__(**data)
