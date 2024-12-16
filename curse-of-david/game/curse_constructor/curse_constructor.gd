extends CanvasLayer


const CURSE_WORD_BUTTON = preload("res://game/curse_constructor/curse_word_button/curse_word_button.tscn")


var word_positions: Array = []
var available_words: Array[Curse.Words] = [Curse.Words.DAMAGE, Curse.Words.SLOWDOWN, Curse.Words.TIME, Curse.Words.TARGETS, Curse.Words.VAMPIRISM]


@onready var line_2d = $Node2D/Line2D
@onready var button_container = $ButtonContainer


var first_button = true
var first_press_flag = true

var new_curse: Curse = Curse.new()


signal curse_ready(curse: Curse)


func init(new_available_words: Array[Curse.Words]) -> void:
	available_words = new_available_words.duplicate()


func _ready():
	for i in 7:
		if i == 3:
			word_positions.append(Vector2.UP.rotated(TAU / 7 * i) * 450 - Vector2.ONE * 128 + Vector2(256, 0))
		elif i == 4:
			word_positions.append(Vector2.UP.rotated(TAU / 7 * i) * 450 - Vector2.ONE * 128 - Vector2(256, 0))
		else:
			word_positions.append(Vector2.UP.rotated(TAU / 7 * i) * 450 - Vector2.ONE * 128)
	generate_new_buttons()


func generate_new_buttons():
	available_words.shuffle()
	word_positions.shuffle()
	for i in clamp(word_positions.size(), 0, clamp(available_words.size(), 2, 3)):
		var new_button = CURSE_WORD_BUTTON.instantiate()

		new_button.position = word_positions[i]

		var word = available_words[i]
		var value
		match word:
			Curse.Words.DAMAGE:
				value = randi_range(5, 10)
			Curse.Words.SLOWDOWN:
				value = snappedf(randf_range(0.1, 0.25), 0.01)
			Curse.Words.TIME:
				value = randi_range(2, 5)
			Curse.Words.TARGETS:
				value = randi_range(5, 10)
			Curse.Words.VAMPIRISM:
				value = true

		new_button.init(word, value)
		button_container.add_child(new_button)
		new_button.button_was_pressed.connect(button_pressed)


func button_pressed(button, word, value):
	if button.first_button and first_press_flag:
		return

	word_positions.erase(button.position)

	var colors = line_2d.gradient.colors
	colors.append(button.color)
	line_2d.gradient.colors = colors

	var gradient_points: PackedFloat32Array = []
	for i in line_2d.gradient.colors.size():
		gradient_points.append(1.0 / line_2d.gradient.colors.size() * i)
	line_2d.gradient.offsets = gradient_points

	if button.first_button:
		line_2d.closed = true
		finish_curse()
		return

	var points = line_2d.points
	points.append(button.position + Vector2.ONE * 128)
	line_2d.points = points


	match word:
		Curse.Words.DAMAGE:
			new_curse.damage += value
		Curse.Words.SLOWDOWN:
			new_curse.slowdown_percentage += value
		Curse.Words.TIME:
			new_curse.lifetime += value
		Curse.Words.TARGETS:
			new_curse.targets_number += value
		Curse.Words.VAMPIRISM:
			new_curse.vampirism = true
			available_words.erase(Curse.Words.VAMPIRISM)

	if first_button:
		first_press_flag = true
		first_button = false
		button.set_first_button()

	if not button.first_button:
		first_press_flag = false

	for btn in button_container.get_children():
		btn.remove()

	generate_new_buttons()


func finish_curse():
	line_2d.modulate.a = 1
	new_curse.line_2d = line_2d.duplicate()
	curse_ready.emit(new_curse)
	queue_free()
