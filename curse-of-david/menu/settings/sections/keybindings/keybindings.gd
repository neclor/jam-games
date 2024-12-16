extends Control


const INPUT_KEY_BUTTON: PackedScene = preload("res://menu/settings/sections/keybindings/input_key_button/input_key_button.tscn")


const ACTION: Dictionary = {
	"zoom_in": "Zoom In",
	"zoom_out": "Zoom Out",
	"move_up": "Move Up",
	"move_down": "Move Down",
	"move_left": "Move Left",
	"move_right": "Move Right",
}


@onready var v_box_container: VBoxContainer = $MarginContainer/VBoxContainer/ScrollContainer/VBoxContainer


func _ready():
	for action in ACTION:
		var new_input_key_button: PanelContainer = INPUT_KEY_BUTTON.instantiate()
		new_input_key_button.action = action
		new_input_key_button.action_name = ACTION[action]
		v_box_container.add_child(new_input_key_button)


func _on_reset_button_pressed():
	InputMap.load_from_project_settings()
	for input_key_button in v_box_container.get_children():
		input_key_button.update_key_text()
