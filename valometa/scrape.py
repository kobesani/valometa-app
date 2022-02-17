from datetime import datetime
from typing import Iterator, List, Optional

import parsel

from pydantic.dataclasses import dataclass

@dataclass
class MatchBasic:
    timestamp: datetime
    url: str
    match_id: int
    event: str


class DateExtractor(object):
    """
    A class extracting the dates from the vlr.gg/matches/results pages

    Attributes
    ----------
    selector: parsel.Selector
        a parsel Selector on which one can call xpath and getall methods
    
    Methods
    -------
    yield_data() -> Iterator[str]
        returns dates in text format from a results page at vlr.gg 

    """

    def __init__(self, selector: parsel.Selector) -> None:
        self.selector = selector

    def yield_data(self) -> Iterator[str]:
        data = (
            self
            .selector
            .xpath("//div[@class='wf-label mod-large']")
            .xpath("normalize-space(./text())")
            .getall()
        )

        for datum in data:
            yield datum


class CardExtractor(object):
    def __init__(self, selector: parsel.Selector) -> None:
        self.selector = selector

    def yield_data(self) -> List[parsel.Selector]:
        data = (
            self
            .selector
            .xpath("//div[@class='wf-card']")
        )

        for datum in data:
            yield datum


class MatchExtractor(object):
    def __init__(self, selector: parsel.Selector) -> None:
        self.selector = selector
        self.date_extractor = DateExtractor(self.selector)
        self.card_extractor = CardExtractor(self.selector)

    def build_timestamp(self, date: str, match: parsel.Selector):
        time = (
            match
            .xpath("./div[@class='match-item-time']")
            .xpath("normalize-space(./text())")
            .get()
        )

        utc_offset = (
            datetime
            .utcnow()
            .astimezone()
            .utcoffset()
            .total_seconds()
        )

        utc_offset_hours = int(utc_offset / 3600)

        return datetime.strptime(
            f"{date}, {time} UTC+{utc_offset_hours:02}:00",
            "%a, %B %d, %Y, %I:%M %p %Z%z"
        )

    def event_name(self, match: parsel.Selector) -> Optional[str]:
        return (
            Event(match).yield_data()
        )

    def yield_data(self):
        for date, card in zip(
            self.date_extractor.yield_data(),
            self.card_extractor.yield_data()
        ):
            for match in (
                card.xpath("./a[contains(@class, 'wf-module-item match-item')]")
            ):

                yield MatchBasic(
                    timestamp=self.build_timestamp(date, match),
                    url=match.attrib['href'],
                    match_id=int(match.attrib['href'].split("/")[1]),
                    event=self.event_name(match)
                )


class Event(object):
    def __init__(self, selector: parsel.Selector):
        self.selector = selector

    def yield_data(self) -> Optional[str]:
        return (
            self
            .xpath("./div[@class='match-item-event text-of']")
            .xpath("normalize-space(./text()[last()])")
            .get()
        )
