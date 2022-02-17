"""
This module contains classes which yields non-selector data types from a
specified base selector (upon class creation). Here, non-selector simply means
that xpath or get(all) methods will not be called on the data that is yielded in
the yield_data method of the class

"""

from typing import Iterator

import parsel


class DateExtractor(object):
    """
    A class extracting the dates from the vlr.gg/matches/results pages

    Attributes
    ----------
    selector: parsel.Selector
        the parsel Selector created using the response.text (i.e. the main
        selector), needs xpath and getall methods
    
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