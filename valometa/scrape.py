from typing import Iterator

import parsel

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



class ResultsCardScraper:
    pass


class MatchScraper:
    pass