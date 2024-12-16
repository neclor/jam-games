class_name Player
extends Entity


func move() -> void:
	move_direction_vector = Vector2(Input.get_axis("move_left", "move_right"), Input.get_axis("move_up", "move_down"))
	move_direction_vector.y /= 2
	super.move()


func die():
	dead = true
	Signals.game_over.emit()
	get_tree().paused = true
