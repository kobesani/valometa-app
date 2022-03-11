from datetime import date
from typing import List

from pydantic import BaseModel, confloat, validator, ValidationError, root_validator

from valometa.data.raw import (
    min_patch_version, max_patch_version
)

patch_constraint = confloat(
    ge=min_patch_version, le=max_patch_version
)

class DateRange(BaseModel):
    date_begin: date
    date_end: date


class NumberMatchesDay(BaseModel):
    date_of_count: date
    count: int


class PatchConstraintError(Exception):
    pass


class MapPatchFilter(BaseModel):
    map_name: str
    patch_lower: patch_constraint = min_patch_version
    patch_upper: patch_constraint = max_patch_version

    @root_validator
    def lower_le_upper(cls, values):
        lower, upper = (
            values.get('patch_lower'), values.get('patch_upper')
        )

        # Nones if the confloat fails for lower or upper
        if lower is not None and upper is not None:
            if lower > upper:
                raise PatchConstraintError(
                    f"lower={lower} > upper={upper} not allowed."
                )

        return values



