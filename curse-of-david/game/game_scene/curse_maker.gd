extends Node

const CURSE_CONSTRUCTOR = preload("res://game/curse_constructor/curse_constructor.tscn")

const NEW_WORD = preload("res://game/new_word/new_word.tscn")
var available_words: Array[Curse.Words] = [Curse.Words.DAMAGE, Curse.Words.SLOWDOWN]


@onready var player = %Player
@onready var enemy_container = %EnemyContainer


func _ready():
	create_new_curse()

	Signals.enemy_dead.connect(check_new_word)




func create_new_curse():
	var new_curse_constructor = CURSE_CONSTRUCTOR.instantiate()
	new_curse_constructor.init(available_words)
	add_child(new_curse_constructor)
	new_curse_constructor.curse_ready.connect(curse_created)


func curse_created(curse: Curse):
	var enemies = enemy_container.get_children()
	enemies.sort_custom(func(a, b): return player.global_position.distance_squared_to(a.global_position) < player.global_position.distance_squared_to(b.global_position))

	for i in clamp(curse.targets_number, 0, enemies.size()):
		var new_course = Curse.new()
		new_course.player = player
		new_course.line_2d = curse.line_2d.duplicate()
		new_course.damage = curse.damage
		new_course.slowdown_percentage = curse.slowdown_percentage
		new_course.vampirism = curse.vampirism
		new_course.targets_number = curse.targets_number
		new_course.lifetime = curse.lifetime

		enemies[i].add_child(new_course)

	create_new_curse()


func check_new_word():
	if get_parent().enemy_count == 10:
		available_words.append(Curse.Words.TIME)
		var new_word = NEW_WORD.instantiate()
		new_word.init(Curse.Words.TIME)

		get_parent().add_child(new_word)


	elif get_parent().enemy_count == 50:
		available_words.append(Curse.Words.VAMPIRISM)
		var new_word = NEW_WORD.instantiate()
		new_word.init(Curse.Words.VAMPIRISM)

		get_parent().add_child(new_word)


	elif get_parent().enemy_count == 100:
		available_words.append(Curse.Words.TARGETS)
		var new_word = NEW_WORD.instantiate()
		new_word.init(Curse.Words.TARGETS)

		get_parent().add_child(new_word)
