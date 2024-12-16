extends Node2D


@onready var left_marker = $LeftMarker
@onready var right_marker = $RightMarker

@onready var light = $Light
@onready var left_arrow = $LeftArrow
@onready var right_arrow = $RightArrow


const LIGHT_ON = preload("res://assets/light_on.png")
const LIGHT_OFF = preload("res://assets/light_off.png")

@onready var key_fragment = $Key_fragment
@onready var key_fragment_2 = $Key_fragment2
@onready var key_fragment_3 = $Key_fragment3
@onready var key_fragment_4 = $Key_fragment4

var fragments = []
var collected := false

var rng := RandomNumberGenerator.new()


var corridors := [1]
var current_corridor_index := 0
var last_corridor_index = 0

var key_room_index



func _ready():
	hide_arrows()
	rng.randomize()
	seed(rng.seed)

	for i in randi_range(7, 11):
		corridors.append(randi_range(0, 1))

	key_room_index = randi_range(3, corridors.size() - 3)

	corridors[key_room_index] = 1

	fragments = [key_fragment, key_fragment_2, key_fragment_3, key_fragment_4]

func _physics_process(_delta):
	if collected:
		$Sprite2D.visible = true

func switch_light():
	Sfx.play_switch()
	if corridors[current_corridor_index] == 0:
		corridors[current_corridor_index] = 1
		light.turn_on_light(1)
	else:
		corridors[current_corridor_index] = 0
		light.turn_off_light()

func _input(_event):
	if Input.is_action_just_pressed("action") and light.somebody_close:
		switch_light()
	elif Input.is_action_just_pressed("action") and $door/Label.visible:
		Sfx.play_door()
		get_tree().change_scene_to_file("res://game/locations/rooms/end_room/end_room.tscn")
		GlobalAudioStreamPlayer.stop()


func _on_left_door_body_entered(body):
	body.position = right_marker.position
	Sfx.play_door()
	
	last_corridor_index = current_corridor_index
	
	if current_corridor_index == 0:
		current_corridor_index = corridors.size() - 1
	else:
		current_corridor_index -= 1

	light.check_light(corridors[current_corridor_index])

func _on_right_door_body_entered(body):
	body.position = left_marker.position
	Sfx.play_door()
	last_corridor_index = current_corridor_index
	
	if current_corridor_index == corridors.size() - 1:
		current_corridor_index = 0
	else:
		current_corridor_index += 1

	light.check_light(corridors[current_corridor_index])

func hide_arrows():
	left_arrow.visible = false
	right_arrow.visible = false

func show_arrow(i):
	if i == 0:
		left_arrow.visible = true
	else:
		right_arrow.visible = true


func _on_door_body_entered(_body):
	if collected:
		$door/Label.visible = true

func _on_door_body_exited(_body):
	if collected:
		$door/Label.visible = false

