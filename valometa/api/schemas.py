import enum

from datetime import date
from typing import List, Literal

from pydantic import BaseModel, confloat, root_validator

from valometa.data.raw import (
    min_patch_version,
    max_patch_version,
)


class MapOptions(str, enum.Enum):
    Fracture = 'Fracture'
    Split = 'Split'
    Ascent = 'Ascent'
    Breeze = 'Breeze'
    Bind = 'Bind'
    Icebox = 'Icebox'
    Haven = 'Haven'
    All = 'All'


class AgentOptions(str, enum.Enum):
    brimstone = "brimstone"
    viper = "viper"
    omen = "omen"
    killjoy = "killjoy"
    cypher = "cypher"
    sova = "sova"
    sage = "sage"
    phoenix = "phoenix"
    jett = "jett"
    reyna = "reyna"
    raze = "raze"
    breach = "breach"
    skye = "skye"
    yoru = "yoru"
    astra = "astra"
    kayo = "kayo"
    chamber = "chamber"
    neon = "neon"


patch_constraint = confloat(
    ge=min_patch_version, le=max_patch_version
)

class DateRange(BaseModel):
    date_begin: date
    date_end: date


class NumberMatchesDay(BaseModel):
    date_of_count: date
    count: int


class MapPatchFilter(BaseModel):
    map_name: MapOptions
    patch_lower: patch_constraint = min_patch_version
    patch_upper: patch_constraint = max_patch_version

    @root_validator
    def lower_le_upper(cls, values):
        lower, upper = (
            values.get('patch_lower'), values.get('patch_upper')
        )

        if lower is not None and upper is not None:
            assert lower < upper, f"lower={lower} > upper={upper} not allowed."

        return values


class AgentPickCount(BaseModel):
    agent_name: AgentOptions
    pick_count: int


class AllAgentPicks(BaseModel):
    pick_rates: List[AgentPickCount]
    map_name: MapOptions
    patches: List[patch_constraint]
