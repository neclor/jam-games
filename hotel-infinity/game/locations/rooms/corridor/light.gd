extends Node2D


@onready var e_label = $ELabel
@onready var light_sprite = $LightSprite

@onready var ghost = $"../Ghost"
@onready var ghost_marker = $"../GhostMarker"

const LIGHT_ON = preload("res://assets/light_on.png")
const LIGHT_OFF = preload("res://assets/light_off.png")

var somebody_close := false

var corridor

func _ready():
	corridor = get_parent()

func check_light(number):
	corridor.hide_arrows()
	if number == 0:
		turn_off_light()
	else:
		turn_on_light()

func turn_on_light(e = 0):
	light_sprite.texture = LIGHT_ON
	corridor.modulate = Color("ffffff")
	ghost.turn_off()
	ghost.position = ghost_marker.position
	corridor.hide_arrows()

	if e == 1 and corridor.current_corridor_index == corridor.key_room_index:
		var flag = true
		for i in corridor.fragments:
			if i.is_work == true:
				flag = false
		if flag:
			corridor.collected = true
		else:
			get_node("/root/EndlessCorridor/Character").key_number = 0
	
	elif e == 0:
		if corridor.last_corridor_index == corridor.key_room_index and corridor.corridors[corridor.key_room_index] == 0:
			var flag = true
			for i in corridor.fragments:
				if i.is_work == true:
					flag = false
			if flag:
				corridor.collected = true
			else:
				get_node("/root/EndlessCorridor/Character").key_number = 0
	
	for i in corridor.fragments:
			i.off()

func turn_off_light():
	light_sprite.texture = LIGHT_OFF
	corridor.modulate = Color("404040")
	ghost.position = ghost_marker.position
	ghost.turn_on()

	if corridor.current_corridor_index < corridor.key_room_index:
		corridor.show_arrow(1)
		get_node("/root/EndlessCorridor/Character").key_number = 0
		if corridor.last_corridor_index == corridor.key_room_index and corridor.corridors[corridor.key_room_index] == 0:
			var flag = true
			for i in corridor.fragments:
				if i.is_work == true:
					flag = false
			if flag:
				corridor.collected = true
			else:
				get_node("/root/EndlessCorridor/Character").key_number = 0
		for i in corridor.fragments:
			i.off()
	elif corridor.current_corridor_index > corridor.key_room_index:
		corridor.show_arrow(0)
		get_node("/root/EndlessCorridor/Character").key_number = 0
		if corridor.last_corridor_index == corridor.key_room_index and corridor.corridors[corridor.key_room_index] == 0:
			var flag = true
			for i in corridor.fragments:
				if i.is_work == true:
					flag = false
			if flag:
				corridor.collected = true
			else:
				get_node("/root/EndlessCorridor/Character").key_number = 0
		for i in corridor.fragments:
			i.off()
	elif !corridor.collected:
		for i in corridor.fragments:
			print(i)
			i.on()

func _on_area_2d_body_entered(_body):
	e_label.visible = true
	somebody_close = true

func _on_area_2d_body_exited(_body):
	e_label.visible = false
	somebody_close = false








