
from typing import List
import parsel


class AgentsExtractor(object):
    def __init__(self, selector: parsel.SelectorList) -> None:
        self.selector = selector

    def yield_data(self) -> List[str]:
        return (
            self
            .selector
            .xpath("./div/div/table/tbody/tr")
            .xpath("./td[@class='mod-agents']/div/span/img/@title")
            .getall()
        )


class PlayerIdsExtractor(object):
    def __init__(self, selector: parsel.SelectorList) -> None:
        self.selector = selector

    def yield_data(self) -> List[int]:
        return [
            int(x) for x in (
                self
                .selector
                .xpath("./div/div/table/tbody/tr")
                .xpath("td[@class='mod-player']/div/a/@href")
                # extract player id from URL /player/<id>/<name>
                .re("/(\d+)/")
            )
        ]


class MapNamesExtractor(object):
    def __init__(self, selector: parsel.SelectorList) -> None:
        self.selector = selector

    def yield_data(self) -> List[str]:
        return (
            self
            .selector
            .xpath("./div[@class='vm-stats-game-header']")
            .xpath("./div[@class='map']/div/span")
            .xpath("normalize-space(./text())")
            .getall()
        )


class TeamIdsExtractor(object):
    def __init__(self, selector: parsel.Selector) -> None:
        self.selector = selector

    def yield_data(self) -> List[int]:
        return [
            int(x) for x in (
                self
                .selector
                .xpath("//a[contains(@class, 'match-header-link wf-link-hover mod-')]")
                .xpath("@href")
                # extract team id from URL /team/<id>/<name>
                .re("/(\d+)/")
            )
        ]

class GameIdsExtractor(object):
    def __init__(self, selector: parsel.SelectorList) -> None:
        self.selector = selector

    def yield_data(self) -> List[int]:
        return [
            int(x) for x in (
                self
                .selector
                .xpath('@data-game-id')
                .getall()
            )
        ]


class PatchExtractor(object):
    def __init__(self, selector: parsel.Selector) -> None:
        self.selector = selector

    def yield_data(self) -> str:
        first_try = (
            self
            .selector
            .xpath("//div/div[@class='wf-tooltip']")
            .xpath("normalize-space(./text())")
            .get()
        )

        if first_try is None:
            return (
                self
                .selector
                .xpath("//div[@class='match-header-date']")
                .xpath("./div[@style='margin-top: 4px;']")
                .xpath("./div[@style='font-style: italic;']")
                .xpath("normalize-space(./text())")
                .get()
            )

        return first_try
