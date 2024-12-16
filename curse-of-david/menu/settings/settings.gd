extends CanvasLayer

@onready var tab_container = $MarginContainer/TabContainer

func _on_tab_container_tab_selected(tab: int) -> void:
	if tab == 0:
		self.visible = false
		tab_container.current_tab = 1
