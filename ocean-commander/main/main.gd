extends Node

const MAP = preload("res://game/map/map.tscn")

var map
@onready var h_box_container: HBoxContainer = $CanvasLayer/Hud/MarginContainer/VBoxContainer/HBoxContainer/HBoxContainer


func _ready():
	Signals.restart_game.connect(prepare_game)
	prepare_game()
	pass


func prepare_game():
	Global.game_over = true
	$CanvasLayer/Control.visible = true
	h_box_container.visible = false
	if map:
		map.queue_free()
	map = MAP.instantiate()
	map.modulate = Global.color
	add_child(map)
	get_tree().paused = true


func _on_button_pressed() -> void:
	h_box_container.visible = true
	$CanvasLayer/Control.visible = false
	Global.game_over = false
	get_tree().paused = false
