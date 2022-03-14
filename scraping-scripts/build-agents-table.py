#! /usr/bin/env python3

from valometa.scrape import AgentsBuild

agents_db_builder = AgentsBuild(overwrite=True)
agents_db_builder.build_database()
