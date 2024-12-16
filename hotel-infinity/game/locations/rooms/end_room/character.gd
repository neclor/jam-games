extends "res://game/character/character.gd"

func dead():
	get_tree().change_scene_to_file("res://ui/end.tscn")
