extends Node2D

var value: int 
var color: Color

@onready var points_label: Label = $PointsContainer/PointsLabel


func set_value(new_value: int, new_color: Color) -> void:
	value = new_value
	color = new_color


func _ready() -> void:
	points_label.text = str(value)
	points_label.modulate = color


func remove() -> void:
	queue_free()
