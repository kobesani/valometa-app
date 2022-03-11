from typing import Optional

import pandas


def get_matches_per_day(
    match_cards_dataframe: pandas.DataFrame
) -> pandas.DataFrame:
    return (
        match_cards_dataframe
        .groupby(match_cards_dataframe.timestamp.dt.date)
        .size()
        .reset_index()
        .rename(columns={0: 'count'})
    )


def get_agent_pick_rates(
    agents_dataframe: pandas.DataFrame,
    map_name: str,
    patch_lower: float,
    patch_upper: float
) -> pandas.DataFrame:
    patch_filter = (
        agents_dataframe
        .query(f'patch <= {patch_upper}')
        .query(f'patch >= {patch_lower}')
    )

    if map_name != "All":
        map_filter = patch_filter.query(f'map_name == {map_name}')
    
    else:
        map_filter = patch_filter

    return (
        map_filter
        .groupby(['agent_name'])
        .size()
        .reset_index()
    )
