
from datetime import datetime


class Tournament(object):
    DATE_FORMAT = "%Y.%m.%d"

    def __init__(self, name, year=None, month=None, start=None, end=None,
                 atp_url=None, earning=None, winners=(), location=None,
                 type_=None):
        self.name = name
        self.year = year
        self.month = month
        self.start = datetime.strptime(start, self.DATE_FORMAT)
        self.end = datetime.strptime(end, self.DATE_FORMAT)
        self.atp_url = atp_url
        self.earning = earning
        self.winners = dict(
            single=winners.get("single"),
            double=winners.get("double")
        )
        self.location = location
        self.type = type_


class Player(object):
    def __init__(self, name, age=None, rank=None, atp_url=None):
        self.name = name
        self.age = age
        self.rank = rank
        self.atp_url = atp_url
