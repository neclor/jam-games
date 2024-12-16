extends Control


const RESOLUTION = [
	
	
]


const WINDOW: Array[String] = [
	"Window",
	"Borderless Window",
	"Fullscreen",
]


@onready var resolution_option_button: OptionButton = $MarginContainer/ScrollContainer/VBoxContainer/Resolution/OptionButton
@onready var window_option_button: OptionButton = $MarginContainer/ScrollContainer/VBoxContainer/Window/OptionButton


func _on_resolution_option_button_item_selected(index: int) -> void:
	pass # Replace with function body.


func _on_window_option_button_item_selected(index: int) -> void:
	pass # Replace with function body.
