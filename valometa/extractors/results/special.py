from datetime import datetime
from typing import Optional

import parsel
import pendulum

DEFAULT_TIMEZONE = pendulum.timezone('Europe/Vienna')


class Timestamp(object):
    def __init__(self, selector: parsel.Selector, date: str) -> None:
        self.date = date
        self.selector = selector

        self.current_timezone = pendulum.now().tzinfo

        # utc_offset_seconds = (
        #     datetime
        #     .utcnow()
        #     .astimezone()
        #     .utcoffset()
        #     .total_seconds()
        # )

        # self.utc_offset = int(utc_offset_seconds / 3600)

        # assert self.utc_offset == utc_offset_seconds / 3600, (
        #     "UTC offset is not a whole hour number"
        # )

    def yield_data(self) -> Optional[datetime]:
        time_data = (
            self
            .selector
            .xpath("./div[@class='match-item-time']")
            .xpath("normalize-space(./text())")
            .get()
        )

        if not time_data:
            return None
        
        ts = f"{self.date}, {time_data}"

        return self.timezone.convert(
            pendulum.from_format(
                ts, "ddd, MMMM DD, YYYY, hh:mm A", tz=DEFAULT_TIMEZONE
            )
        )

        # return datetime.strptime(
        #     f"{self.date}, {time} UTC+{self.utc_offset:02}:00",
        #     "%a, %B %d, %Y, %I:%M %p %Z%z"
        # )
