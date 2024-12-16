class_name Entity
extends CharacterBody2D


const POPUP_POINTS: PackedScene = preload("res://game/entities/base_entity/popup_points/popup_points.tscn")


@export_group("Health")
@export var max_hp: int = 100
@export var hp: int = 100


@export_group("Speed")
@export var speed: int = 1000
var speed_multiplier: float = 1


var move_direction_vector: Vector2 = Vector2.ZERO


var dead: bool = false


@onready var sprite_2d: Sprite2D = $SpriteContainer/Sprite2D
@onready var move_animation_player: AnimationPlayer = $SpriteContainer/MoveAnimationPlayer
@onready var effect_animation_player: AnimationPlayer = $EffectAnimationPlayer


func _physics_process(_delta) -> void:
	move()


func _process(_delta) -> void:
	move_animation()


func move_animation() -> void:
	if move_direction_vector == Vector2.ZERO:
		#move_animation_player.stop()
		#return
		pass

	if move_direction_vector.x != 0:
		sprite_2d.flip_h = true if move_direction_vector.x < 0 else false

	move_animation_player.play("move")


func create_normalized_isometric_vector(vector: Vector2) -> Vector2:
	var isometric_vector: Vector2 = Vector2(vector.x, vector.y * 2).normalized()
	isometric_vector.y /= 2
	return isometric_vector


func move() -> void:
	velocity = create_normalized_isometric_vector(move_direction_vector) * speed * speed_multiplier
	move_and_slide()


func create_popup_points(value: int, color: Color) -> void:
	var new_popup_points = POPUP_POINTS.instantiate()
	new_popup_points.set_value(value, color)
	add_child(new_popup_points)


func take_heal(input_heal: int) -> void:
	if input_heal <= 0:
		return
	hp = clamp(hp + input_heal, 0, max_hp)

	create_popup_points(input_heal, Color.GREEN)
	effect_animation_player.play("take_heal")


func take_damage(input_damage: int) -> void:
	if input_damage <= 0:
		return
	hp = clamp(hp - input_damage, 0, max_hp)
	check_death()

	create_popup_points(input_damage, Color.RED)
	effect_animation_player.play("take_damage")


func check_death() -> void:
	if hp > 0:
		return
	die()


func die():
	pass
