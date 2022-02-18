from datetime import datetime

import parsel

class Timestamp(object):
    def __init__(self, selector: parsel.Selector, date: str) -> None:
        self.date = date
        self.selector = selector

        utc_offset_seconds = (
            datetime
            .utcnow()
            .astimezone()
            .utcoffset()
            .total_seconds()
        )

        self.utc_offset = int(utc_offset_seconds / 3600)

        assert self.utc_offset == utc_offset_seconds / 3600, (
            "UTC offset is not a whole hour number"
        )

    def yield_data(self) -> datetime:
        time = (
            self
            .selector
            .xpath("./div[@class='match-item-time']")
            .xpath("normalize-space(./text())")
            .get()
        )

        return datetime.strptime(
            f"{self.date}, {time} UTC+{self.utc_offset_hours:02}:00",
            "%a, %B %d, %Y, %I:%M %p %Z%z"
        )
