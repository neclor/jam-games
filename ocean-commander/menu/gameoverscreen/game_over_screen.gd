extends Control

@onready var label: Label = $CenterContainer/PanelContainer/MarginContainer/VBoxContainer/Label
@onready var label_2: Label = $CenterContainer/PanelContainer/MarginContainer/VBoxContainer/Label2


func _ready() -> void:
		Signals.win.connect(win)
		Signals.game_over.connect(over_game)
		Signals.restart_game.connect(over_game)


func _on_button_pressed() -> void:
	Signals.restart_game.emit()
	self.visible = false


func win():
	self.visible = true
	label.text = "YOU WIN!"
	write_time()

func over_game():
	self.visible = true
	label.text = "YOU LOSE!"
	write_time()

func write_time():
	label_2.text = "Time:\n" + str(Global.minutes) + " : " + str(Global.seconds)
