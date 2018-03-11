
import requests
from bs4 import BeautifulSoup

from objects import Tournament, Player


class AllTournamentsFetcher(object):
    TIMEOUT = 5  # seconds

    HOME_URL = "http://www.atpworldtour.com"
    PATH = "tournaments"

    @classmethod
    def request_data(cls, **params):
        url = "%s/%s" % (cls.HOME_URL, cls.PATH)
        return cls.parse_all_tournaments(BeautifulSoup(
            requests.get(url, timeout=cls.TIMEOUT, params=params).text,
            "html5lib"
        ))

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
                                cls.HOME_URL, div.findChild("a").attrs["href"])
                        )
                    elif div.text.strip().strip("\t").strip("\n") == "DBL":
                        winners["double"] = (
                            Player(
                                name=a.text.strip().strip(
                                    "\t").strip("\n"),
                                atp_url="%s%s" % (
                                    cls.HOME_URL, a.attrs["href"])
                            ) for a in div.findChildren("a")
                        )
                tournaments.append(Tournament(
                    name=row.findChild(
                        "td", {"class": "title-content"}).findChild("a").text,
                    year=year,
                    month=month,
                    atp_url="%s%s" % (cls.HOME_URL, row.findChild(
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
    def parse_all_tournaments(cls, soup):
        tournaments = []
        for child in filter(
                lambda c: "content-accordion" in c.get_attribute_list("class"),
                soup.findAll("div")):  # each month
            month, year = child.findChild(
                "div", {"class": "accordion-label"}).text.split()
            tournaments.extend(cls.parse_tournaments_per_month(
                child, year.strip(), month.strip()))
        return tournaments


class SingleTournamentFetcher(object):
    def __init__(self, tournament):
        """
        Tournament object
        """
        self.tournament = tournament

    def request_data(self, type_):
        if type_ == "overview":
            return self.parse_overview(BeautifulSoup(
                requests.get(self.tournament.atp_url, timeout=5).text,
                "html5lib"
            ))

    def parse_overview(self, soup):
        pass


class RankingParser(object):
    HOME_URL = "http://www.atpworldtour.com/en/rankings"

    PATHS = {
        "single": "single"
    }

    @classmethod
    def request_data(cls, type_):
        return cls.parse_ranking(BeautifulSoup(
            requests.get("%s/%s" % (
                cls.HOME_URL, cls.PATHS[type_]), timeout=5).text,
            "html5lib"
        ))

    @classmethod
    def parse_ranking(cls, soup):
        pass
