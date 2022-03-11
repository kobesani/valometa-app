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


def convert_patch_to_float(
    agents_df: pandas.DataFrame
) -> pandas.DataFrame:
    agents_df['patch'] = (
        agents_df['patch']
        .str
        .replace("Patch ", "")
        .astype(float)
    )

    return agents_df


def get_agent_pick_rates(
    agents_dataframe: pandas.DataFrame,
    patch_lower: float,
    patch_upper: float,
    map_name: Optional[str] = None
) -> pandas.DataFrame:
    patch_filter = (
        convert_patch_to_float(agents_dataframe)
        .query(f'patch <= {patch_upper}')
        .query(f'patch >= {patch_lower}')
    )

    if map_name:
        map_filter = patch_filter.query(f'map_name == \'{map_name}\'')
    
    else:
        map_filter = patch_filter

    return (
        map_filter
        .groupby(['agent_name'])
        .size()
        .to_frame("pick_rate")
        .reset_index()
    )
