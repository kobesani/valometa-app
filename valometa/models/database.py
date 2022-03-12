from datetime import datetime
from typing import Any, Dict, Optional

from pydantic.dataclasses import dataclass

# from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean
)

@dataclass
class MatchItem:
    timestamp: Optional[datetime]
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


@dataclass
class AgentItem:
    match_id: int
    game_id: int
    team_id: int
    player_id: int
    map_name: str
    agent_name: str
    patch: Optional[str]

    def asdict(self) -> Dict[str, Any]:
        return {
            x: self.__dict__[x] for x in self.__dataclass_fields__.keys()
        }


valometa_base = declarative_base()


class Matches(valometa_base):
    __tablename__ = "matches"

    match_id = Column(Integer, primary_key=True)
    url = Column(String)
    timestamp = Column(DateTime, nullable=True)
    stakes = Column(String)
    event = Column(String)
    map_stats = Column(Boolean)
    player_stats = Column(Boolean)


class Agents(valometa_base):
    __tablename__ = "agents"

    match_id = Column(Integer, primary_key=True)
    game_id = Column(Integer, primary_key=True)
    team_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, primary_key=True)
    map_name = Column(String)
    agent_name = Column(String)
    patch = Column(String, nullable=True)
