class_name Ship
extends CharacterBody2D


const CANNONBALL = preload("res://game/ships/cannonball/cannonball.tscn")


@export_group("Health")
@export var max_hp: int = 1
@onready var hp: int = max_hp
var dead: bool = false


@export_group("Speed")
@export var speed: int = 1
var acceleration: float = 0.75
var move_direction: Vector2 = Vector2.ZERO
var destination: bool = false


@export_group("Attack")
@export var attack_power: int = 1
@export_range(1, 3) var attack_cooldown: int = 3
@export var target_group: StringName
var in_combat: bool = false
var target: Node2D = null
@export var cannon: bool = true


@onready var melee_attack_box: Area2D = $MeleeAttackBox
@onready var range_attack_box: Area2D = $RangeAttackBox
@onready var attack_timer: Timer = $AttackTimer


@onready var navigation_agent_2d: NavigationAgent2D = $NavigationAgent2D


@onready var sprite_2d: Sprite2D = $SpriteConatiner/Sprite2D
@onready var color: Color = sprite_2d.modulate


@onready var damage_animation_player: AnimationPlayer = $DamageAnimationPlayer
@onready var rotation_animation_player: AnimationPlayer = $RotationAnimationPlayer
@onready var position_animation_player: AnimationPlayer = $PositionAnimationPlayer


func _ready() -> void:
	attack_timer.wait_time = attack_cooldown
	rotation_animation_player.play("rotate")
	position_animation_player.play("sway")


func _process(_delta) -> void:
	if move_direction == Vector2.ZERO:
		rotation_animation_player.speed_scale = 1
		position_animation_player.speed_scale = 1
	else:
		rotation_animation_player.speed_scale = 2
		position_animation_player.speed_scale = 2

	if move_direction.x < 0:
		sprite_2d.flip_h = false
	elif move_direction.x > 0:
		sprite_2d.flip_h = true


func _physics_process(delta: float) -> void:
	if not dead:
		if (not destination) and (not target) and range_attack_box.has_overlapping_bodies():
			for body in range_attack_box.get_overlapping_bodies():
				if body.is_in_group(target_group) and (not body.dead):
					target = body
					break
		if is_instance_valid(target) and (not target.dead):
			navigation_agent_2d.target_position = target.global_position
		else:
			target = null
		move(delta)


func _on_attack_timer_timeout() -> void:
	var close_combat: bool = false
	if melee_attack_box.has_overlapping_bodies():
		for body in melee_attack_box.get_overlapping_bodies():
			if body.is_in_group(target_group) and (not body.dead):
				body.take_damage(attack_power)
				damage_animation_player.play("take_damage")
				close_combat = true
				in_combat = true
				break
	if range_attack_box.has_overlapping_bodies() and (not close_combat):
		for body in range_attack_box.get_overlapping_bodies():
			if body.is_in_group(target_group) and (not body.dead):
				fire_cannonball(body)
				in_combat = true
				break
	elif not close_combat:
		in_combat = false


func fire_cannonball(target_node: Node) -> void:
	if not cannon:
		return
	var new_cannonball: Cannonball = CANNONBALL.instantiate()
	new_cannonball.modulate = modulate
	var relative_target_position: Vector2 = target_node.global_position - global_position
	var new_velocity
	if target_node is CharacterBody2D:
		new_velocity = Deflection.vector2(new_cannonball.speed, relative_target_position, target_node.velocity)
	else:
		new_velocity = Deflection.vector2(new_cannonball.speed, relative_target_position, Vector2.ZERO)
	if new_velocity == Vector2.ZERO:
		new_velocity = relative_target_position.normalized() * new_cannonball.speed
	new_cannonball.global_position = global_position
	new_cannonball.init(new_velocity, target_group)
	new_cannonball.modulate = color
	get_parent().add_child(new_cannonball)


func move(delta: float) -> void:
	var next_point_relative = navigation_agent_2d.get_next_path_position() - global_position
	if next_point_relative.length_squared() < 256:
		destination = false
		navigation_agent_2d.target_position = global_position
		move_direction = Vector2.ZERO
	else:
		move_direction = next_point_relative.normalized()
	velocity = velocity.lerp(move_direction * speed, acceleration * delta)
	move_and_slide()


func take_damage(input_damage: int) -> void:
	if input_damage <= 0:
		return
	hp = clamp(hp - input_damage, 0, max_hp)
	if hp <= 0:
		die()
	else:
		damage_animation_player.play("take_damage")


func die() -> void:
	pass


func _on_touch_screen_button_pressed() -> void:
	pass


func _on_touch_screen_button_released() -> void:
	pass



func _on_regen_itmer_timeout() -> void:
	if (not in_combat) and (not dead):
		clamp(hp + 10, 0, max_hp)
