extends BaseHomeIsland


@onready var player_ship_container = get_parent().get_parent().get_parent().find_child("PlayerShipContainer")


const PLAYER_BOAT = preload("res://game/ships/player_ships/player_boat.tscn")


func die() -> void:
	if dead:
		return
	Signals.game_over.emit()
	get_tree().paused = true
	dead = true


func work_complete():
	var new_boat = PLAYER_BOAT.instantiate()
	var random_position = Vector2.from_angle(randf_range(0, TAU)).normalized() * 384
	
	new_boat.global_position = global_position + random_position
	player_ship_container.add_child(new_boat)
