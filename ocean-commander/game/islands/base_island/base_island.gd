class_name Island
extends Node2D


enum Sides{
	NOSIDE,
	PLAYER,
	ENEMY,
}
var side = Sides.NOSIDE


enum States {
	IDLE,
	WORK,
}
@export var state: States:
	set(new_state):
		time_passed = 0
		state = new_state
		
@onready var time: Label = $Time

var num_workers: int :
	set(value):
		num_workers = value
		time.text = str(num_workers) + " / 3"


@export var production_time: int = 10
var time_passed: float = 0
@export var product_amount: int = 10


@onready var area_2d: Area2D = $Area2D




func _physics_process(delta: float) -> void:
	match state:
		States.WORK:
			work(delta)


func work(delta: float) -> void:
	time_passed = clamp(time_passed + delta, 0, production_time)
	queue_redraw()
	if time_passed == production_time:
		time_passed = 0
		work_complete()


func work_complete():
	pass



func _draw():
	draw_arc(Vector2.ZERO, 160, - PI / 2, lerpf(- PI / 2, TAU - PI / 2, time_passed / production_time), 128, Color.GRAY, 16)


func _on_area_2d_body_entered(_body: Node2D) -> void:
	check_side()


func _on_area_2d_body_exited(_body: Node2D) -> void:
	check_side()


func check_side():
	if not area_2d.has_overlapping_bodies():
		change_side(Sides.NOSIDE)
	else:
		var player = 0
		var enemy = 0
		for body in area_2d.get_overlapping_bodies():
			if body.is_in_group("player"):
				player += 1
			elif body.is_in_group("enemy"):
				enemy += 1
		if ((not player) and (not enemy)) or (player and enemy):
			change_side(Sides.NOSIDE)
		elif (player):
			change_side(Sides.PLAYER)
		else:
			change_side(Sides.ENEMY)

func change_side(new_side: Sides):
	if side == new_side:
		var workers = 0
		if side == Sides.PLAYER:
			for body in area_2d.get_overlapping_bodies():
				if body.is_in_group("player"):
					workers += 1
		elif side == Sides.ENEMY:
			for body in area_2d.get_overlapping_bodies():
				if body.is_in_group("enemy"):
					workers += 1
		num_workers = clamp(workers, 0, 3)
		return
	side = new_side
	if new_side == Sides.NOSIDE:
		num_workers = 0
		state = States.IDLE
	else:
		var workers = 0
		if side == Sides.PLAYER:
			for body in area_2d.get_overlapping_bodies():
				if body.is_in_group("player"):
					workers += 1
		elif side == Sides.ENEMY:
			for body in area_2d.get_overlapping_bodies():
				if body.is_in_group("enemy"):
					workers += 1
		num_workers = clamp(workers, 0, 3)
		state = States.WORK
	queue_redraw()
