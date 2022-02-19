import os
from sqlite3 import IntegrityError
import time

from typing import Dict, Iterator, Optional

import parsel
import requests

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

from valometa import match_results_url
from valometa.data import sqlite_db_path
from valometa.extractors.results.other import DateExtractor
from valometa.extractors.results.selectors import CardExtractor
from valometa.extractors.results.single import (
    Event,
    Stakes,
    MapStats,
    PlayerStats
)
from valometa.extractors.results.special import Timestamp
from valometa.models.database import MatchItem, Matches, valometa_base


class MatchExtractor(object):
    def __init__(self, selector: parsel.Selector) -> None:
        self.selector = selector
        self.date_extractor = DateExtractor(self.selector)
        self.card_extractor = CardExtractor(self.selector)

    def yield_data(self) -> Iterator[MatchItem]:
        for date, card in zip(
            self.date_extractor.yield_data(),
            self.card_extractor.yield_data()
        ):
            for match in (
                card.xpath("./a[contains(@class, 'wf-module-item match-item')]")
            ):

                yield MatchItem(
                    timestamp=Timestamp(match, date).yield_data(),
                    url=match.attrib['href'],
                    match_id=int(match.attrib['href'].split("/")[1]),
                    event=Event(match).yield_data(),
                    stakes=Stakes(match).yield_data(),
                    player_stats=PlayerStats(match).yield_data(),
                    map_stats=MapStats(match).yield_data()
                )


class MatchesBuild(object):
    def __init__(
        self,
        sqlite_db_path: str = sqlite_db_path, 
        delay: int = 1
    ) -> None:
        self.session = requests.Session()
        self.delay = delay
        self.sqlite_db_path = sqlite_db_path

        self.current_page = 1

        # save first page to do check at the end to make sure it didn't change
        with self.session as sesh:
            response = sesh.get(
                match_results_url.format(page=self.current_page)
            )
            self.first_page_content = response.content

        self.max_pages = int(
            parsel
            .Selector(response.text)
            .xpath("//a[@class='btn mod-page'][last()]/text()")
            .get()
        )

        self.failed_requests: Dict[int, int] = {}

    def set_up_builder(self) -> None:
        try:
            os.remove(sqlite_db_path)
        except FileNotFoundError:
            pass

        self.engine = create_engine(f"sqlite:///{self.sqlite_db_path}")
        self.db_session_maker = sessionmaker(bind=self.engine)
        valometa_base.metadata.create_all(self.engine)

    def request(self) -> Optional[requests.models.Response]:
        with self.session as sesh:
            response = sesh.get(
                match_results_url.format(page=self.current_page)
            )

        self.status_code = response.status_code

        if self.status_code != 200:
            self.failed_requests[self.current_page] = self.status_code
            return None

        return response

    def parse_response(self) -> None:
        response = self.request()

        if response is None:
            return
        
        main_select = parsel.Selector(response.text)
        matches_generator = MatchExtractor(main_select).yield_data()

        for match in matches_generator:
            with self.db_session_maker() as sesh:
                sesh.add(Matches(**match.asdict()))
                try:
                    sesh.commit()
                except IntegrityError as e:
                    # error is raised when games are shifted between pages
                    # due to games finishing and being added to page 1
                    print(e)

    def build_database(self) -> None:
        self.set_up_builder()
        for x in range(1, self.max_pages + 1):
            print(f"Scraping Page {x}")
            self.current_page = x
            self.parse_response()
            time.sleep(self.delay)


class MatchesUpdate(object):
    def __init__(
        self,
        sqlite_db_path: str = sqlite_db_path, 
        delay: int = 1
    ) -> None:

        self.session = requests.Session()
        self.delay = delay
        self.sqlite_db_path = sqlite_db_path    

    def set_up_updater(self) -> None:
        self.engine = create_engine(f"sqlite:///{self.sqlite_db_path}")
        self.db_session_maker = sessionmaker(bind=self.engine)

    def request(self) -> Optional[requests.models.Response]:
        with self.session as sesh:
            response = sesh.get(
                match_results_url.format(page=self.current_page)
            )

        self.status_code = response.status_code

        if self.status_code != 200:
            self.failed_requests[self.current_page] = self.status_code
            return None

        return response

    def parse_response(self) -> None:
        response = self.request()

        if response is None:
            return
        
        main_select = parsel.Selector(response.text)
        matches_generator = MatchExtractor(main_select).yield_data()

        for match in matches_generator:
            with self.db_session_maker() as sesh:
                sesh.add(Matches(**match.asdict()))
                try:
                    sesh.commit()
                except IntegrityError as e:
                    # error is raised when games are shifted between pages
                    # due to games finishing and being added to page 1
                    print(e)

    def update_database(self) -> None:
        self.set_up_builder()
        for x in range(1, self.max_pages + 1):
            print(f"Scraping Page {x}")
            self.current_page = x
            self.parse_response()
            time.sleep(self.delay)

# class ValorantResults:
#     def __init__(self, sqlite_db_path: str, request_delay: int = 1) -> None:
#         self.session: requests.Session = requests.Session()
#         self.current_page: int = 1
#         self.max_pages: Optional[int] = None
#         self.status_code: Optional[int] = None
#         self.delay = request_delay

#         self.sqlite_db_path = sqlite_db_path
#         self.engine = create_engine(f"sqlite:///{self.sqlite_db_path}")
#         self.db_session_maker = sessionmaker(bind=self.engine)
#         # makes sure tables are created (if not already)
#         valorant_scraper_base.metadata.create_all(self.engine)

#         # get most recent match
#         with self.db_session_maker() as sesh:
#             self.latest_match: Optional[datetime] = (
#                 sesh
#                 .query(Matches.timestamp)
#                 .order_by(desc('timestamp'))
#                 .first()
#             )

#         if self.latest_match is None:
#             # set date to earliest date if database is freshly made
#             self.latest_match = datetime(1970, 1, 1, tzinfo=timezone(timedelta(seconds=3600), 'UTC'))
        
#         else:
#             # have to get it out of the tuple
#             self.latest_match = self.latest_match[0].astimezone(
#                 timezone(timedelta(seconds=3600), 'UTC')
#             )

#         self.new_matches: bool = True

#     def request(self) -> Optional[requests.models.Response]:
#         with self.session as sesh:
#             response = sesh.get(
#                 match_results_url.format(page=self.current_page)
#             )

#         if response.status_code != 200:
#             self.status_code = response.status_code
#             return None

#         if self.max_pages is None:
#             self.max_pages = int(
#                 parsel
#                 .Selector(response.text)
#                 .xpath("//a[@class='btn mod-page'][last()]/text()")
#                 .get()
#             )

#         return response