extends Node2D

@onready var animation_player = $AnimationPlayer
const GOLD = preload("res://game/gold.tscn")

var cart_position = 0
var rng = RandomNumberGenerator.new()

func _ready():
	animation_player.play("left_down_0")


func _on_button_0_pressed():
	change_pos(0)

func _on_button_1_pressed():
	change_pos(1)

func _on_button_2_pressed():
	change_pos(2)

func _on_button_3_pressed():
	change_pos(3)

func change_pos(new_pos):
	if new_pos == cart_position:
		return

	match cart_position:
		0:
			animation_player.play_backwards("left_down_0")
		1:
			animation_player.play_backwards("left_up_1")
		2:
			animation_player.play_backwards("right_down_2")
		3:
			animation_player.play_backwards("right_up_3")

	await animation_player.animation_finished
	cart_position = new_pos

	match new_pos:
		0:
			animation_player.play("left_down_0")
		1:
			animation_player.play("left_up_1")
		2:
			animation_player.play("right_down_2")
		3:
			animation_player.play("right_up_3")



var lives = 3
var gold = 0
var speed = 3

func restart():
	call_deferred("rel_scn")

func rel_scn():
	get_tree().reload_current_scene()




func add_gold():
	gold += 1
	update_counter()
	if gold % 10 == 0:
		var new_speed = speed - 0.5 * (gold / 10)
		new_speed = 1.5 if new_speed < 1.5 else new_speed
		$Timer.wait_time = new_speed

func update_counter():
	$CanvasLayer2/GoldCounter.text = "Gold: " + str(gold)

func update_lives():
	var points = [$CanvasLayer2/MarginContainer/HBoxContainer/TextureRect, $CanvasLayer2/MarginContainer/HBoxContainer/TextureRect2, $CanvasLayer2/MarginContainer/HBoxContainer/TextureRect3]
	
	for point in points:
		point.visible = false

	for i in range(lives):
		points[i].visible = true


func sub_life():
	if lives == 0:
		game_over()
		return

	lives -= 1
	update_lives()

func _on_area_2d_body_entered(body):
	sub_life()
	body.queue_free()


func game_over():
	restart()
	pass


var prev_pos = 0

func _on_timer_timeout():
	create_gold(choose_rand_pos())
	
func choose_rand_pos():
	var rnd_pos = rng.randi_range(0, 3)
	if rnd_pos != prev_pos:
		prev_pos = rnd_pos
		return rnd_pos
	else:
		return choose_rand_pos()


func create_gold(pos):
	var new_gold = GOLD.instantiate()

	match pos:
		0:
			$GoldOre.play_anim()
			new_gold.position = $spawn_0.position
		1:
			$GoldOre_1.play_anim()
			new_gold.position = $spawn_1.position
		2:
			$GoldOre_2.play_anim()
			new_gold.position = $spawn_2.position
		3:
			$GoldOre_3.play_anim()
			new_gold.position = $spawn_3.position

	await get_tree().create_timer(0.7).timeout

	add_child(new_gold)









