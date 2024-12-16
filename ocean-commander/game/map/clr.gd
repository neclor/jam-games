extends Node


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	Signals.color_changed.connect(func(new_clr): get_parent().modulate = new_clr)
