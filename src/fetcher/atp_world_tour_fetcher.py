import requests

from bs4 import BeautifulSoup

from objects import Tournament, Player


class ATPWorldTourFetcher(object):
    """
    Fetch the different pages of http://www.atpworldtour.com
    """
    TIMEOUT = 5  # in seconds

    URL = "http://www.atpworldtour.com"
    SUPPORTED_LANGUAGES = {"en", "es"}

    SUPPORTED_PATHS = {
        "tournaments": "tournaments"
    }

    @classmethod
    def make_url(cls, type_, lang=None):
        if type_ not in cls.SUPPORTED_PATHS:
            raise Exception("type not supported. type=%s" % type_)
        if lang is None:
            return "%s/%s" % (cls.URL, cls.SUPPORTED_PATHS[type_])
        elif lang in cls.SUPPORTED_LANGUAGES:
            return "%s/%s/%s" % (cls.URL, lang, cls.SUPPORTED_PATHS[type_])
        else:
            raise Exception("lang not supported. lang=%s" % lang)

    @classmethod
    def request_data(cls, type_, lang=None, **params):
        url = cls.make_url(type_, lang=lang)
        print url
        return cls.parse(
            requests.get(url, timeout=cls.TIMEOUT, params=params), type_)

    @classmethod
    def parse(cls, response, type_):
        if type_ == "tournaments":
            return cls.parse_tournaments(response)

    @classmethod
    def parse_tournaments_per_month(cls, div, year, month):
        tournaments = []
        for row in filter(bool, div.findAll("tr")):
            try:
                start, end = row.findChild(
                    "td", {"class": "title-content"}).findChild(
                    "span", {"class": "tourney-dates"}).text.split("-")
                winners = {}
                print row.select(".tourney-details")
                for div in row.select(".tourney-details > div"):
                    if div.text.strip().strip("\t").strip("\n") == "SGL":
                        winners["single"] = Player(
                            name=div.findChild("a").text.strip().strip(
                                "\t").strip("\n"),
                            atp_url="%s/%s" % (
                                cls.URL, div.findChild("a").attrs["href"])
                        )
                    elif div.text.strip().strip("\t").strip("\n") == "DBL":
                        winners["double"] = (
                            Player(
                                name=a.text.strip().strip(
                                    "\t").strip("\n"),
                                atp_url="%s/%s" % (
                                    cls.URL, a.attrs["href"])
                            ) for a in div.findChildren("a")
                        )
                tournaments.append(Tournament(
                    name=row.findChild(
                        "td", {"class": "title-content"}).findChild("a").text,
                    year=year,
                    month=month,
                    atp_url="%s/%s" % (cls.URL, row.findChild(
                        "td", {"class": "title-content"}).findChild(
                        "a").attrs["href"]),
                    start=start.strip().strip("\t").strip("\n"),
                    end=end.strip().strip("\t").strip("\n"),
                    location=row.findChild(
                        "td", {"class": "title-content"}).findChild(
                        "span", {
                            "class": "tourney-location"
                        }).text.strip().strip("\t").strip("\n"),
                    winners=winners
                ))
            except (AttributeError, ValueError):
                continue
        return tournaments

    @classmethod
    def parse_tournaments(cls, response):
        soup = BeautifulSoup(response.text, "html5lib")
        tournaments = []
        for child in filter(
                lambda c: "content-accordion" in c.get_attribute_list("class"),
                soup.findAll("div")):  # each month
            month, year = child.findChild(
                "div", {"class": "accordion-label"}).text.split()
            tournaments.extend(cls.parse_tournaments_per_month(
                child, year.strip(), month.strip()))
        return tournaments
