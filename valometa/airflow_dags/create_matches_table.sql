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
