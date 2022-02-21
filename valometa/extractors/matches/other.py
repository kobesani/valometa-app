
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