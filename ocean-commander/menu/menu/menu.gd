extends Control



func _on_texture_button_toggled(toggled_on: bool) -> void:
	if toggled_on:
		AudioServer.set_bus_mute(0, true)

	else:
		AudioServer.set_bus_mute(0, false)



func _on_color_picker_color_changed(color: Color) -> void:
	Signals.color_changed.emit(color)
