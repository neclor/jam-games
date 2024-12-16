class_name Shipyard
extends Island

const ENEMY_BRIGANTINE = preload("res://game/ships/enemy_ships/enemy_brigantine.tscn")
const ENEMY_GALLEON = preload("res://game/ships/enemy_ships/enemy_galleon.tscn")
const PLAYER_BRIGANTINE = preload("res://game/ships/player_ships/player_brigantine.tscn")
const PLAYER_GALLEON = preload("res://game/ships/player_ships/player_galleon.tscn")


@onready var player_ship_container = get_parent().get_parent().get_parent().find_child("PlayerShipContainer")
@onready var enemy_ship_container = get_parent().get_parent().get_parent().find_child("EnemyShipContainer")


@export var brigantine: bool


var product_ship = null
var prod_side: Sides


func _physics_process(delta: float) -> void:
	if state == States.WORK:
		work(delta)
		return

	if side == Sides.NOSIDE:
		return

	if side == Sides.PLAYER:
		prod_side = Sides.PLAYER
		if brigantine:
			product_ship = PLAYER_BRIGANTINE
		else:
			product_ship = PLAYER_GALLEON
	else:
		prod_side = Sides.ENEMY
		if brigantine:
			product_ship = ENEMY_BRIGANTINE
		else:
			product_ship = ENEMY_GALLEON

	if brigantine:
		if side == Sides.PLAYER and Global.player_gold >= 150 and Global.player_wood >= 100:
			Signals.player_got_gold.emit(-150)
			Signals.player_got_wood.emit(-100)
			state = States.WORK
		elif side == Sides.ENEMY and Global.enemy_gold >= 150 and Global.enemy_wood >= 100:
			Signals.enemy_got_gold.emit(-150)
			Signals.enemy_got_wood.emit(-100)
			state = States.WORK
	else:
		if side == Sides.PLAYER and Global.player_gold >= 150 and Global.player_wood >= 200:
			Signals.player_got_gold.emit(-150)
			Signals.player_got_wood.emit(-200)
			state = States.WORK
		elif side == Sides.ENEMY and Global.enemy_gold >= 150 and Global.enemy_wood >= 200:
			Signals.enemy_got_gold.emit(-150)
			Signals.enemy_got_wood.emit(-200)
			state = States.WORK


func work(delta: float) -> void:
	time_passed = clamp(time_passed + delta, 0, production_time)
	queue_redraw()
	if time_passed == production_time:
		time_passed = 0
		work_complete()


func work_complete():
	state = States.IDLE
	var new_ship = product_ship.instantiate()
	
	var random_position = Vector2.from_angle(randf_range(0, TAU)).normalized() * 384
	
	new_ship.global_position = global_position + random_position
	product_ship = null
	if prod_side == Sides.PLAYER:
		player_ship_container.add_child(new_ship)
	else:
		enemy_ship_container.add_child(new_ship)


func change_side(new_side: Sides):
	if side == new_side:
		return
	side = new_side
