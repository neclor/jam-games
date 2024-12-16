class_name Projectile
extends CharacterBody2D


@export var damage: int = 20
@export var speed: int = 1750


func init(new_velocity: Vector2) -> void:
	velocity = new_velocity


func _physics_process(delta) -> void:
	var colision: KinematicCollision2D = move_and_collide(velocity * delta)
	if colision:
		var collider: Node = colision.get_collider()
		if collider.is_in_group("player"):
			collider.take_damage(damage)
		queue_free()
