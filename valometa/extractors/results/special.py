from datetime import datetime
from typing import Optional

import parsel
import pendulum

DEFAULT_TIMEZONE = pendulum.timezone('Europe/Vienna')


class Timestamp(object):
    def __init__(self, selector: parsel.Selector, date: str) -> None:
        self.date = date
        self.selector = selector

        self.current_timezone = pendulum.now().timezone

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

        return DEFAULT_TIMEZONE.convert(
            pendulum.from_format(
                ts, "ddd, MMMM DD, YYYY, hh:mm A", tz=self.current_timezone
            )
        )
