extends Control



@onready var settings = $Settings

@onready var animation_player = $TextureRect/AnimationPlayer
@onready var animation_player2 = $TextureRect2/AnimationPlayer
@onready var story = $Story


func _on_button_pressed():
	story.visible = true


func _on_button_2_pressed():
	settings.visible = true


func _on_button_mouse_entered():
	animation_player.play("waiting")


func _on_button_mouse_exited():
	animation_player.stop()


func _on_button2_mouse_entered():
	animation_player2.play("waiting")


func _on_button2_mouse_exited():
	animation_player2.stop()
