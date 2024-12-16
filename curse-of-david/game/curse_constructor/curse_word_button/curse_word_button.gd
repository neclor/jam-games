extends TextureButton

signal button_was_pressed(button, word, value)


var word: Curse.Words
var color: Color
var text: String
var value
var first_button = false

@onready var animation_player: AnimationPlayer = $AnimationPlayer
@onready var label: Label = $MarginContainer/Label


func init(new_word: Curse.Words, new_value):
	value = new_value
	word = new_word
	match word:
		Curse.Words.DAMAGE:
			text = "Damage\n+" + str(new_value)
			color = Color.BLUE_VIOLET
		Curse.Words.SLOWDOWN:
			text = "Speed\n-" + str(new_value * 100) + "%"
			color = Color.BLUE
		Curse.Words.TIME:
			text = "Time\n+" + str(new_value)
			color = Color.AQUA
		Curse.Words.TARGETS:
			text = "Targets\n+" + str(new_value)
			color = Color.ORANGE
		Curse.Words.VAMPIRISM:
			color = Color.CRIMSON
			text = "Vampirism"



func _ready() -> void:
	animation_player.play("waiting")
	label.text = text
	self_modulate = color
	label.set("theme_override_colors/font_color", Color.WHITE)


func _on_mouse_entered() -> void:
	#animation_player.stop()
	self_modulate = Color.WHITE
	label.set("theme_override_colors/font_color", Color.BLACK)


func _on_mouse_exited() -> void:
	#animation_player.play("waiting")
	if not first_button:
		self_modulate = color
		label.set("theme_override_colors/font_color", Color.WHITE)



func _on_pressed():
	button_was_pressed.emit(self, word, value)


func set_first_button():
	first_button = true
	label.text = "END"
	self_modulate = Color.WHITE


func remove():
	if not first_button:
		queue_free()
