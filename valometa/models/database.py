from datetime import datetime
from typing import Any, Dict

from pydantic.dataclasses import dataclass

from sqlalchemy.orm import declarative_base

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean
)

@dataclass
class MatchItem:
    timestamp: datetime
    url: str
    match_id: int
    event: str
    stakes: str
    map_stats: bool
    player_stats: bool

    def asdict(self) -> Dict[str, Any]:
        return {
            x: self.__dict__[x] for x in self.__dataclass_fields__.keys()
        }


valometa_base = declarative_base()

class Matches(valometa_base):
    __tablename__ = "matches"

    match_id = Column(Integer, primary_key=True)
    url = Column(String)
    timestamp = Column(DateTime)
    stakes = Column(String)
    event = Column(String)
    map_stats = Column(Boolean)
    player_stats = Column(Boolean)