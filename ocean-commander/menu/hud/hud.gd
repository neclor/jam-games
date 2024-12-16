extends Control

@onready var gold: Label = %Label2
@onready var wood: Label = %Label
@onready var menu: Control = $MarginContainer/VBoxContainer/Control/Menu

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	Signals.player_got_gold.connect(update_gold)
	Signals.player_got_wood.connect(update_wood)
	Signals.color_changed.connect(clr)


func update_gold(_a):
	gold.text = str(Global.player_gold)
	
func update_wood(_a):
	wood.text = str(Global.player_wood)


func _on_texture_button_toggled(toggled_on: bool) -> void:
	if toggled_on:
		Signals.pause_game.emit()
		menu.visible = true
	else:
		Signals.resume_game.emit()
		menu.visible = false
		

func clr(new_color):
	$MarginContainer/VBoxContainer/HBoxContainer.modulate = new_color
