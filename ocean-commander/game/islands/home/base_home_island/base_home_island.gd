class_name BaseHomeIsland
extends Island


@export_group("Health")
@export var max_hp: int = 500
@onready var hp: int = max_hp



var dead: bool = false


func _physics_process(delta: float) -> void:
	time_passed = clamp(time_passed + delta, 0, production_time)
	queue_redraw()
	if time_passed == production_time:
		time_passed = 0
		work_complete()


func work_complete():
	pass




func take_damage(input_damage: int) -> void:
	if input_damage <= 0:
		return
	hp = clamp(hp - input_damage, 0, max_hp)
	if hp <= 0:
		die()


func die() -> void:
	pass


func _on_regen_timer_timeout() -> void:
	if not dead:
		clamp(hp + 10, 0, max_hp)


func _on_area_2d_body_entered(body: Node2D) -> void:
	pass


func _on_area_2d_body_exited(body: Node2D) -> void:
	pass
