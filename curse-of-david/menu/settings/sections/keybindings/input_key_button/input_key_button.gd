extends PanelContainer


var action: String
var action_name: String


var waiting_input: bool = false

@onready var label: Label = $HBoxContainer/Label
@onready var button: Button = $HBoxContainer/Button


func _ready() -> void:
	label.text = action_name
	update_key_text()


func _on_button_pressed() -> void:
	if not waiting_input:
		waiting_input = true
		button.text = "..."


func _input(event: InputEvent) -> void:
	if waiting_input and (event is InputEventKey or (event is InputEventMouseButton and event.is_pressed())):
		if event is InputEventMouseButton:
			event.double_click = false
		InputMap.action_erase_events(action)
		InputMap.action_add_event(action, event)

		waiting_input = false
		update_key_text()
		accept_event()


func update_key_text() -> void:
	var events = InputMap.action_get_events(action)
	button.text = events[0].as_text().trim_suffix(" (Physical)") if events.size() > 0 else ""
