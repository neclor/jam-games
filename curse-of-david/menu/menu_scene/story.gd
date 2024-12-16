extends CanvasLayer

const GAME = preload("res://game/game_scene/game.tscn")
const STORY_2 = preload("res://assets/sprites/Story/Story2.png")

@onready var texture_rect = $TextureRect

var a = false


func _on_button_pressed():
	if a:
		get_tree().change_scene_to_packed(GAME)
	a = true
	texture_rect.texture = STORY_2
