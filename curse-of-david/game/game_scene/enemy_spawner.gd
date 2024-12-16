extends Node


var enemies = [
	preload("res://game/entities/enemies/melee_enemies/spearman/spearman.tscn"),
	#preload("res://game/entities/enemies/wizard/wizard.tscn")
]
var a = preload("res://game/entities/enemies/melee_enemies/knight/knight.tscn")
var b = preload("res://game/entities/enemies/wizard/wizard.tscn")
var king = preload("res://game/entities/enemies/melee_enemies/king/king.tscn")



@onready var timer: Timer = $Timer
@onready var enemy_container: Node2D = %EnemyContainer
@onready var player: Player = %Player
@onready var timer_2 = $Timer2


var timer_flag = false


func _on_timer_timeout():
	create_enemy()


func _ready():
	Signals.enemy_dead.connect(check_deaths)



func create_enemy():
	var new_enemy: Enemy = enemies.pick_random().instantiate()
	new_enemy.init(player)
	enemy_container.add_child(new_enemy)



func check_deaths():
	if get_parent().enemy_count == 10:
		enemies.append(a)
		timer.wait_time = 1.5

	elif get_parent().enemy_count == 50:
		enemies.append(b)

		timer.wait_time = 1

	elif get_parent().enemy_count == 100:
		timer.wait_time = 0.75
		timer_2.start()

	if get_parent().enemy_count >= 100 and get_parent().enemy_count % 100 == 0:
		spawn_king()



func _on_timer_2_timeout():
	timer.wait_time = timer.wait_time - 0.1
	
	
	
func spawn_king():
	var new_enemy: Enemy = king.instantiate()
	new_enemy.init(player)
	enemy_container.add_child(new_enemy)
	
