extends PanelContainer


const WINDOW_RESOLUTION: Dictionary = {
	"1280 × 720": Vector2i(1280, 720),
	"1920 × 1080": Vector2i(1920, 1080),
	"2560 × 1440": Vector2i(2560, 1440),
	"3840 × 2160": Vector2i(3840, 2160),
	"7680 × 4320": Vector2i(7680, 4320),
}


@onready var option_button: OptionButton = $HBoxContainer/OptionButton


func _ready() -> void:
	for window_resolution in WINDOW_RESOLUTION:
		option_button.add_item(window_resolution)


func _on_option_button_item_selected(index: int) -> void:
	DisplayServer.window_set_size(WINDOW_RESOLUTION[option_button.get_item_text(index)])
