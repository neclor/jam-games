class_name Cannonball
extends CharacterBody2D


@export_group("Speed")
@export var speed: int = 200
@export var max_distance: int = 1024
var distance: float = 0


@export_group("Attack")
@export var attack_power: int = 10
var target_group: String


@onready var area_2d: Area2D = $Area2D


func init(new_velocity: Vector2, new_target_group: StringName) -> void:
	target_group = new_target_group
	velocity = new_velocity


func _physics_process(delta) -> void:
	move_and_slide()
	distance += speed * delta
	if distance >= max_distance:
		queue_free()


func _draw():
	draw_circle(Vector2.ZERO, 16, Color.WHITE)


func _on_area_2d_body_entered(body: Node2D) -> void:
	if body.is_in_group(target_group):
		body.take_damage(attack_power)
		queue_free()
