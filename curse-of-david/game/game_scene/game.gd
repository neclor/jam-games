extends Node2D

var time: float = 0
var seconds: int = 0
var minutes: int = 0


#const MENU = load("res://menu/menu_scene/menu.tscn")


var enemy_count: int = 0

@onready var player = %Player

@onready var timer = %Timer
#@onready var panel = $GameHud/Panel
@onready var panel = $GameHud/Panel
@onready var animation_player = $GameHud/MarginContainer/VBoxContainer/Control/TextureRect/AnimationPlayer
@onready var hp = $GameHud/MarginContainer/VBoxContainer/Hp
@onready var button = $GameHud/MarginContainer/VBoxContainer/Control/TextureRect2/Button
@onready var animation_player2 = $GameHud/MarginContainer/VBoxContainer/Control/TextureRect2/AnimationPlayer
@onready var texture_rect_2 = $GameHud/MarginContainer/VBoxContainer/Control/TextureRect2


func _ready():
	Signals.enemy_dead.connect(enemy_died)


func _physics_process(delta: float):
	time += delta
	seconds = fmod(time, 60)
	minutes = fmod(time, 3600) / 60
	timer.text = str(minutes) + " : " + str(seconds) + " kill: " + str(enemy_count)
	hp.text = str(player.hp)


func _on_button_pressed():
	if not player.dead:
		get_tree().paused = not get_tree().paused
		panel.visible = not panel.visible
		texture_rect_2.visible = not texture_rect_2.visible


func enemy_died():
	enemy_count += 1


func _on_button_mouse_entered():
	animation_player.play("waiting")


func _on_button_mouse_exited():
	animation_player.stop()


func _on_button2_mouse_entered():
	animation_player2.play("waiting")


func _on_button2_mouse_exited():
	animation_player2.stop()


func _on_button2_pressed():
	get_tree().paused = false
	get_tree().change_scene_to_file("res://menu/menu_scene/menu.tscn")
