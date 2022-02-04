import pandas

def get_matches_per_day(match_cards_dataframe: pandas.DataFrame) -> pandas.DataFrame:
    return (
        match_cards_dataframe
        .groupby(match_cards_dataframe.timestamp.dt.date)
        .size()
        .reset_index()
        .rename(columns={'0': 'count'})
    )