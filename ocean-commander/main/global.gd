extends Node

var ship_pressed: bool = false

var player_gold: int = 0
var enemy_gold: int = 0

var player_wood: int = 0
var enemy_wood: int = 0




var time: float = 0
var seconds: int = 0
var minutes: int = 0

var camera
var color = Color.WHITE

var game_over

func _ready() -> void:
	Signals.player_got_gold.connect(func(amount: int): player_gold += amount)
	Signals.enemy_got_gold.connect(func(amount: int): enemy_gold += amount)
	
	Signals.player_got_wood.connect(func(amount: int): player_wood += amount)
	Signals.enemy_got_wood.connect(func(amount: int): enemy_wood += amount)


	Signals.pause_game.connect(pause)
	Signals.resume_game.connect(unpause)
	Signals.win.connect(over_game)
	Signals.game_over.connect(over_game)
	Signals.restart_game.connect(over_game)
	Signals.color_changed.connect(func(new_col): color = new_col)



func over_game():
	game_over = true


func pause():
	if not game_over:
		get_tree().paused = true

func unpause():
	if not game_over:
		get_tree().paused = false





func restart():
	game_over = false
	get_tree().paused = false

	player_gold= 0
	enemy_gold = 0
	player_wood = 0
	enemy_wood = 0

	Signals.player_got_gold.emit(0)
	Signals.enemy_got_gold.emit(0)
	
	Signals.player_got_wood.emit(0)
	Signals.enemy_got_wood.emit(0)
