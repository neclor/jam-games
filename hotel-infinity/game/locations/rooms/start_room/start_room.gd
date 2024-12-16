extends Node2D

@onready var character = $Character




func _on_right_door_body_entered(_body):
	Sfx.play_door()
	change_scene()
	
func change_scene():
	get_tree().change_scene_to_file("res://game/locations/rooms/corridor/endless_corridor.tscn")
