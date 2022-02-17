from datetime import datetime
from typing import Iterator, List, Optional

import parsel

from valometa.models.database import MatchItem
from valometa.extractors.results.other import DateExtractor
from valometa.extractors.results.selectors import CardExtractor
from valometa.extractors.results.single import (
    Event,
    Stakes,
    MapStats,
    PlayerStats
)


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

        # all offsets should be divisible by 3600 seconds (1 hour)
        utc_offset_hours = int(utc_offset / 3600)

        # the :02 in the f-string gives zero padding to offset
        return datetime.strptime(
            f"{date}, {time} UTC+{utc_offset_hours:02}:00",
            "%a, %B %d, %Y, %I:%M %p %Z%z"
        )

    def yield_data(self):
        for date, card in zip(
            self.date_extractor.yield_data(),
            self.card_extractor.yield_data()
        ):
            for match in (
                card.xpath("./a[contains(@class, 'wf-module-item match-item')]")
            ):

                yield MatchItem(
                    timestamp=self.build_timestamp(date, match),
                    url=match.attrib['href'],
                    match_id=int(match.attrib['href'].split("/")[1]),
                    event=Event(match).yield_data(),
                    stakes=Stakes(match).yield_data(),
                    player_stats=PlayerStats(match).yield_data(),
                    map_stats=MapStats(match).yield_data()
                )
