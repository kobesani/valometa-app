CREATE TABLE IF NOT EXISTS matches (
	match_id INTEGER NOT NULL, 
	url VARCHAR, 
	timestamp DATETIME, 
	stakes VARCHAR, 
	event VARCHAR, 
	map_stats BOOLEAN, 
	player_stats BOOLEAN, 
	PRIMARY KEY (match_id)
);

CREATE TABLE IF NOT EXISTS agents (
	match_id INTEGER NOT NULL, 
	game_id INTEGER NOT NULL, 
	team_id INTEGER NOT NULL, 
	player_id INTEGER NOT NULL, 
	map_name VARCHAR, 
	agent_name VARCHAR, 
	patch VARCHAR, 
	PRIMARY KEY (match_id, game_id, team_id, player_id)
);
