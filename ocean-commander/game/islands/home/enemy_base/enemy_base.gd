extends BaseHomeIsland


@onready var enemy_ship_container = get_parent().get_parent().get_parent().find_child("EnemyShipContainer")


const ENEMY_BOAT = preload("res://game/ships/enemy_ships/enemy_boat.tscn")


func work_complete():
	var new_boat = ENEMY_BOAT.instantiate()
	
	
	var random_position = Vector2.from_angle(randf_range(0, TAU)).normalized() * 384
	new_boat.global_position = global_position + random_position
	enemy_ship_container.add_child(new_boat)



func die() -> void:
	if dead:
		return
	Signals.win.emit()
	dead = true
