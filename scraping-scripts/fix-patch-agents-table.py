#! /usr/bin/env python3

from valometa.scrape import AgentsBuild

agents_db_builder = AgentsBuild(overwrite=False, backup=True)
agents_db_builder.fix_patch_info()
