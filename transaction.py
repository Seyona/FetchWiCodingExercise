from pydantic import BaseModel
from points import Point


class Transaction(BaseModel):
    payer_name: str
    points: Point

    def __init__(self, name: str, points: int, date_str: str):
        data = {'payer_name': name, 'points': Point(points, date_str)}
        super().__init__(**data)