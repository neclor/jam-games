extends CanvasLayer

var MENU = load("res://menu/menu_scene/menu.tscn")


var flag_king = false
var flag_pause = false

var game_over = false

@onready var timer = $Timer

@onready var label = $Panel/Panel/Label



func _ready():
	Signals.game_over.connect(game_over_func)
	Signals.king_dead.connect(king_dead)


func game_over_func():
	self.visible = true
	game_over = true
	timer.start()
	label.text = "You are dead\n" + "you lived: " + str(get_parent().minutes) + " : " + str(get_parent().seconds) + "\n" + "you killed: " + str(get_parent().enemy_count)


func king_dead():
	if not flag_king:
		self.visible = true
		timer.start()
		flag_king = true
		get_tree().pause = true
		label.text = "Congratulations\nyou have completed the game\nnow you can continue playing endlessly"



func _on_button_button_down():
	if not flag_pause:
		return

	if not game_over:
		flag_pause = false
		self.visible = false
		get_tree().pause = false
		return

	if game_over:
		get_tree().change_scene_to_packed(MENU)


func _on_timer_timeout():
	flag_pause = true
