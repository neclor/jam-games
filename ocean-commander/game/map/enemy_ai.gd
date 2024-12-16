extends Node


var target_index = 0
var target_list = [
	Vector2(410, -1720),
	Vector2(1780, -430),
	Vector2(1780, 600),
	Vector2(-1100, -1790),
	Vector2(400, -890),
	Vector2(-780, -930),
]


var player_base = Vector2(-1200, 1150)


func _ready():
	Signals.enemy_boat_apeared.connect(boat_ai)
	Signals.enemy_warship_apeared.connect(warship_ai)


func boat_ai(boat: Ship):
	boat.navigation_agent_2d.target_position = target_list[target_index]
	target_index = (target_index + 1) % 6

func warship_ai(boat: Ship):
	boat.navigation_agent_2d.target_position = player_base
