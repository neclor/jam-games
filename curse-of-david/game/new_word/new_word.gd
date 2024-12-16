extends CanvasLayer

var color = Color.WHITE
var word= ""

var text = ""

@onready var animation_player = $AnimationPlayer

@onready var texture_rect = $Control/Panel/TextureRect



@onready var label = $Control/Panel/TextureRect/MarginContainer/Label

@onready var desr = $Control/Panel/desr

func init(new_word):
	match new_word:
		Curse.Words.TIME:
			word = "Time"
			color = Color.AQUA
			text = "\nIncreases curse lifetime"
		Curse.Words.TARGETS:
			word = "Targets"
			color = Color.ORANGE
			text = "\nIncreases the number of targets for the curse"
		Curse.Words.VAMPIRISM:
			color = Color.CRIMSON
			word = "Vampirism"
			text = "\nAdds vampirism to curse"

func _ready():
	animation_player.play("waiting")
	get_tree().paused = true
	texture_rect.self_modulate = color
	label.text = word
	desr.text += text

var aaa = false
func _on_button_button_down():
	if aaa:
		
		get_tree().paused = false
		queue_free()


func _on_timer_timeout():
	aaa = true
	pass # Replace with function body.
