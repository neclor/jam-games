extends Node

var player_ships_defeated: int = 0
var enemy_ships_defeated: int = 0


func _ready() -> void:
	Signals.player_ship_died.connect(func(): player_ships_defeated += 1)
	Signals.enemy_ship_died.connect(func(): enemy_ships_defeated += 1)
