import os
import time

from datetime import datetime, timedelta, timezone
from loguru import logger
from typing import Dict, Iterator, Optional

import parsel
import requests

from sqlalchemy import create_engine, desc, exc
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
    """
    A class for building the matches table coming from the
    vlr.gg/matches/results pages

    Attributes
    ----------
    sqlite_db_path: str
        the path where the sqlite database will be placed, old database at this
        path will be deleted when running the initialization step.

    delay: int
        The number of seconds to wait between sending requests to vlr.gg.
    
    Methods
    -------
    yield_data() -> Iterator[parsel.Selector]
        returns the cards (as selectors) under each date on the vlr.gg match results pages

    set_up_builder() -> None
        Method to delete old database, set up new one

    request() -> Optional[requests.models.Response]
        Sends request to vlg.gg/matches/results/page ...

    parse_response() -> None
        Parses response content, extracts match card information and adds it
        to the database in the matches table.

    """

    def __init__(
        self,
        sqlite_db_path: str = sqlite_db_path, 
        delay: int = 1,
    ) -> None:
        self.session = requests.Session()
        self.delay = delay
        self.sqlite_db_path = sqlite_db_path
        self.total_matches: int = 0

        self.current_page = 1
        self.current_url = match_results_url.format(page=self.current_page)

        # save first page to do check at the end to make sure it didn't change
        with self.session as sesh:
            response = sesh.get(self.current_url)
            self.first_page_content = response.content

        self.max_pages = int(
            parsel
            .Selector(response.text)
            .xpath("//a[@class='btn mod-page'][last()]/text()")
            .get()
        )

        logger.info(f"Total number of results pages on vlr.gg = {self.max_pages}")

        if os.path.exists(sqlite_db_path):
            logger.info(f"Removing db at {sqlite_db_path}")
            os.remove(sqlite_db_path)

        self.engine = create_engine(f"sqlite:///{self.sqlite_db_path}")
        self.db_session_maker = sessionmaker(bind=self.engine)
        valometa_base.metadata.create_all(self.engine)

        self.failed_requests: Dict[int, int] = {}

    def request(self) -> Optional[requests.models.Response]:
        with self.session as sesh:
            response = sesh.get(self.current_url)

        self.status_code = response.status_code

        if self.status_code != 200:
            self.failed_requests[self.current_page] = self.status_code
            logger.warning(
                f"Request to {self.current_url} returned status code {response.status_code}"
            )
            return None

        # apply delay here
        time.sleep(self.delay)
        logger.info(f"Scraping page {self.current_url} - {response.status_code}")

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
                    self.total_matches += 1
                except exc.IntegrityError as e:
                    # error is raised when games are shifted between pages
                    # due to games finishing and being added to page 1
                    print(e)

    def build_database(self) -> None:
        for x in range(1, self.max_pages + 1):
            self.current_page = x
            self.current_url = match_results_url.format(page=self.current_page)
            self.parse_response()

        logger.info("Results page parsing, db table build finished")
        logger.info(f"Number of matches parsed: {self.total_matches}")

    def __call__(self) -> None:
        self.build_database()


class MatchesUpdate(object):
    def __init__(
        self,
        sqlite_db_path: str = sqlite_db_path, 
        delay: int = 1
    ) -> None:

        self.session = requests.Session()
        self.delay = delay
        self.sqlite_db_path = sqlite_db_path
        self.latest_match: Optional[datetime] = None
        self.update_finished: bool = False
        self.matches_added: int = 0

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

    def set_up_updater(self) -> None:
        self.engine = create_engine(f"sqlite:///{self.sqlite_db_path}")
        self.db_session_maker = sessionmaker(bind=self.engine)
        
        # get most recent match
        with self.db_session_maker() as sesh:
            self.latest_match = (
                sesh
                .query(Matches.timestamp)
                # sometimes timestamp isn't found and therefore is None, filter
                .filter(Matches.timestamp.is_not(None))
                .order_by(desc('timestamp'))
                # datetime returned as tuple
                .first()[0]
                .astimezone(timezone(timedelta(seconds=3600), 'UTC'))
            )

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
            if match.timestamp < self.latest_match:
                self.update_finished = True
                print("Update should be finished now")
                return
            with self.db_session_maker() as sesh:
                sesh.add(Matches(**match.asdict()))
                try:
                    sesh.commit()
                except exc.IntegrityError as e:
                    # non-unique primary key entry
                    # error is triggered when the database is updated
                    # last match accessed is the last one added to previous db
                    continue
            self.matches_added += 1

    def update_database(self) -> None:
        self.set_up_updater()
        for x in range(1, self.max_pages + 1):
            print(f"Scraping Page {x}")
            self.current_page = x
            self.parse_response()

            if self.update_finished:
                print(f"Update finished: {self.matches_added} matches added.")
                return

            time.sleep(self.delay)
