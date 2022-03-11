"""
This module contains classes which yield new selectors or selector lists based 
on a specified base selector (done upon class creation). These selectors work
on match pages with URLs such as the following:

https://www.vlr.gg/69788/tenstar-vs-kova-vrl-northern-europe-polaris-season-round-3/?game=70664&tab=overview
"""

import parsel


class GameStatContainer(object):
    """
    A class extracting the game stats containers (containing agent lists) from
    the vlr.gg match result home page.

    Attributes
    ----------
    selector: parsel.Selector
        the parsel Selector created using the response.text (i.e. the main
        selector), needs xpath method for extracting data.
    
    Methods
    -------
    yield_data() -> parsel.SelectorList
        returns selectors for the stats containers for maps that were actually
        played in the series, should work on all series types (Bo1, Bo3, Bo5).

    """
    def __init__(self, selector: parsel.Selector) -> None:
        self.selector = selector

    def yield_data(self) -> parsel.SelectorList:
        return (
            self
            .selector
            # check that data-game-id is a number and not just 'all'
            .xpath("//div[contains(@class, 'vm-stats-game ') and re:test(@data-game-id, '^\d+$')]")
        )
