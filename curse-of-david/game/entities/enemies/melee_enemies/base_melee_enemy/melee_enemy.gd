class_name MeleeEnemy
extends Enemy


@onready var area_2d: Area2D = $Area2D


func _on_attack_cooldown_timeout() -> void:
	attack_ready = true
	for body in area_2d.get_overlapping_bodies():
		if body.is_in_group("player"):
			body.take_damage(damage)


func _on_area_2d_body_entered(body):
	if attack_ready and body.is_in_group("player"):
		body.take_damage(damage)
