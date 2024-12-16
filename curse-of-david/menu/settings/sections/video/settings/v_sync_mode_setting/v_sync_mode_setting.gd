extends PanelContainer


const V_SYNC_MODE: Dictionary = {
	"Disabled": DisplayServer.VSYNC_DISABLED,
	"Enabled": DisplayServer.VSYNC_ENABLED,
	"Adaptive": DisplayServer.VSYNC_ADAPTIVE,
	"Mailbox": DisplayServer.VSYNC_MAILBOX,
}


@onready var option_button: OptionButton = $HBoxContainer/OptionButton


func _ready() -> void:
	for v_sync_mode in V_SYNC_MODE:
		option_button.add_item(v_sync_mode)


func _on_option_button_item_selected(index: int) -> void:
	DisplayServer.window_set_vsync_mode(V_SYNC_MODE[option_button.get_item_text(index)])
