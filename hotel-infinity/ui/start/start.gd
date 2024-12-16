extends Control

@onready var button = $Button
@onready var animation_player = $AnimationPlayer




func _on_button_pressed():
	button.visible = false
	animation_player.play("start")


func _on_animation_player_animation_finished(_anim_name):
	get_tree().change_scene_to_file("res://game/locations/rooms/start_room/start_room.tscn")
	GlobalAudioStreamPlayer.play()
