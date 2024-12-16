extends PanelContainer


const WINDOW_MODE: Dictionary = {
	"Window": DisplayServer.WINDOW_MODE_WINDOWED,
	"Fullscreen": DisplayServer.WINDOW_MODE_FULLSCREEN,
	"Exclusive Fullscreen": DisplayServer.WINDOW_MODE_EXCLUSIVE_FULLSCREEN,
}


@onready var option_button: OptionButton = $HBoxContainer/OptionButton


func _ready() -> void:
	for window_mode in WINDOW_MODE:
		option_button.add_item(window_mode)


func _on_option_button_item_selected(index: int) -> void:
	DisplayServer.window_set_mode(WINDOW_MODE[option_button.get_item_text(index)])
