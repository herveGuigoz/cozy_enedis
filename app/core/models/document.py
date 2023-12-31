from datetime import datetime


class Document:
    def __init__(
        self, id=None, minute=0, hour=0, day=0, month=0, year=0, load=0.0, price=None
    ):
        self.id = id
        self.minute = minute
        self.hour = hour
        self.day = day
        self.month = month
        self.year = year
        self.load = load
        self.price = price

    @classmethod
    def from_dict(cls, value):
        return cls(
            id=value.get("_id"),
            minute=value.get("minute", 0),
            hour=value.get("hour", 0),
            day=value.get("day", 0),
            month=value.get("month", 0),
            year=value.get("year", 0),
            load=value.get("load", 0.0),
            price=value.get("price"),
        )

    def get_date(self):
        return self.get_timestamp().isoformat()

    def get_timestamp(self):
        return datetime(self.year, self.month, self.day, self.hour, self.minute)
