import os

import pandas

valorant_tables_dir = os.path.dirname(__file__)

def load_valorant_table(name: str):
    return pandas.read_csv(
        f"{valorant_tables_dir}/{name}.txt", sep='\t'
    )

patch_columns = ['Patch', 'Release']

agent_columns = ['Name', 'Type', 'Patch']

map_columns = ['Name', 'Patch']


valorant_agents_table = (
    load_valorant_table('agents').filter(agent_columns)
)

valorant_maps_table = (
    load_valorant_table('maps').filter(map_columns)
)

valorant_patches_table = (
    load_valorant_table('patches').filter(patch_columns)
)

valorant_patches_table['Release'] = pandas.to_datetime(
    valorant_patches_table['Release']
)


valorant_agents_table['Patch'] = (
    valorant_agents_table['Patch']
    .str
    .replace('Beta', '0.47')
    .astype(float)
)

valorant_maps_table['Patch'] = (
    valorant_maps_table['Patch']
    .str
    .replace('Beta', '0.47')
    .astype(float)
)

# get the release date for the agents and maps
valorant_agents_table = valorant_agents_table.merge(
    valorant_patches_table, on='Patch', how='left'
)

valorant_maps_table = valorant_maps_table.merge(
    valorant_patches_table, on='Patch', how='left'
)

valorant_tables = {
    'agents': valorant_agents_table,
    'maps': valorant_maps_table,
    'patches': valorant_patches_table
}

# setting some useful values that can be imported
current_number_of_agents = len(valorant_agents_table)
current_number_of_maps = len(valorant_maps_table)
min_patch_version = valorant_patches_table['Patch'].min()
max_patch_version = valorant_patches_table['Patch'].max()
