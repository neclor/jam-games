class_name Enemy
extends Entity


@export var damage: int = 10
@export var keep_distance: int = 128

var attack_ready: bool = false
var target: Entity


@onready var attack_cooldown = $AttackCooldown


func init(new_target: Entity = null) -> void:
	target = new_target


func move() -> void:
	if target:
		move_direction_vector = global_position.direction_to(target.global_position)
		if global_position.distance_to(target.global_position) <= keep_distance:
			move_direction_vector = Vector2.ZERO
		super.move()


func _on_attack_cooldown_timeout() -> void:
	attack_ready = true


func die():
	if dead:
		return
	Signals.enemy_dead.emit()
	dead = true
	attack_cooldown.stop()
	sprite_2d.visible = false
	await effect_animation_player.animation_finished
	queue_free()
