extends Enemy


const BASE_PROJECTILE = preload("res://game/objects/projectiles/base_projectile/base_projectile.tscn")


func _on_attack_cooldown_timeout() -> void:
	attack_ready = true
	attack()


func attack() -> void:
	var new_projectile: Projectile = BASE_PROJECTILE.instantiate()
	new_projectile.damage = damage
	var not_isometric_target_position: Vector2 = Vector2(target.global_position.x - global_position.x, (target.global_position.y - global_position.y) * 2)
	var not_isometric_target_velocity: Vector2 = Vector2(target.velocity.x, target.velocity.y * 2)

	var new_velocity = Deflection.vector2(new_projectile.speed, not_isometric_target_position,not_isometric_target_velocity)

	if new_velocity == Vector2.ZERO: #or randi_range(0, 1) == 1:
		new_velocity = global_position.direction_to(not_isometric_target_position) * new_projectile.speed

	new_velocity = Vector2(new_velocity.x, new_velocity.y / 2)
	new_projectile.global_position = global_position
	new_projectile.init(new_velocity)
	get_parent().get_parent().find_child("ObjectConatiner").add_child(new_projectile)

	attack_ready = false
