"""
This module contains classes which yield new selectors from a specified base
selector (upon class creation)
"""

from typing import Iterator

import parsel


class CardExtractor(object):
    """
    A class extracting the cards (containing matches) from the
    vlr.gg/matches/results pages

    Attributes
    ----------
    selector: parsel.Selector
        the parsel Selector created using the response.text (i.e. the main
        selector), needs xpath method for extracting data
    
    Methods
    -------
    yield_data() -> Iterator[parsel.Selector]
        returns the cards (as selectors) under each date on the vlr.gg match results pages

    """

    def __init__(self, selector: parsel.Selector) -> None:
        self.selector = selector

    def yield_data(self) -> Iterator[parsel.Selector]:
        data = (
            self
            .selector
            .xpath("//div[@class='wf-card']")
        )

        for datum in data:
            yield datum
