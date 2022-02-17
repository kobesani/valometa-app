"""
Classes defined here also take selectors upon initialization, however they yield
a single piece of data (not an iterable)
"""

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