"""
Classes defined here also take selectors upon initialization, however they yield
a single piece of data (not an iterable)
"""

from optparse import Option
import parsel

from typing import Optional


class Event(object):
    def __init__(self, selector: parsel.Selector):
        self.selector = selector

    def yield_data(self) -> Optional[str]:
        return (
            self
            .selector
            .xpath("./div[@class='match-item-event text-of']")
            .xpath("normalize-space(./text()[last()])")
            .get()
        )


class Stakes(object):
    def __init__(self, selector: parsel.Selector) -> None:
        self.selector = selector

    def yield_data(self) -> Optional[str]:
        return (
            self
            .selector
            .xpath("./div[@class='match-item-event text-of']")
            .xpath("./div[@class='match-item-event-series text-of']")
            .xpath("normalize-space(./text())")
            .get()
        )


class MapStats(object):
    def __init__(self, selector: parsel.Selector) -> None:
        self.selector = selector

    def yield_data(self) -> Optional[bool]:
        stats = (
            self
            .selector
            .xpath("./div[@class='match-item-vod']/div[@class='wf-tag mod-big']")
            .xpath("normalize-space(./text())")
            .getall()
        )

        for stat in stats:
            if stat == "Map":
                return True
        
        return False


class PlayerStats(object):
    def __init__(self, selector: parsel.Selector) -> None:
        self.selector = selector

    def yield_data(self) -> Optional[bool]:
        stats = (
            self
            .selector
            .xpath("./div[@class='match-item-vod']/div[@class='wf-tag mod-big']")
            .xpath("normalize-space(./text())")
            .getall()
        )

        for stat in stats:
            if stat == "Player":
                return True

        return False
