class_name Curse
extends Node2D


enum Words {
	DAMAGE,
	SLOWDOWN,
	TIME,
	TARGETS,
	VAMPIRISM,
}


var lifetime: int = 1
var time: int = 0


var damage: int = 0
var slowdown_percentage: float = 0
var slowdown_var: float
var vampirism: bool = false
var targets_number: int = 5


var player: Player

var timer: Timer = Timer.new()
var line_2d: Line2D


func _ready():
	scale = Vector2.ONE * 0.75
	add_child(line_2d)

	timer.wait_time = 1
	add_child(timer)
	timer.timeout.connect(_on_timer_timeout)
	timer.start()

	if get_parent().is_in_group("enemy"):
		slowdown_var = slowdown_percentage * get_parent().speed_multiplier
		get_parent().speed_multiplier -= slowdown_var


func _process(delta):
	rotation += PI / 2 * delta
	pass



func _on_timer_timeout():
	if get_parent().is_in_group("enemy"):
		get_parent().take_damage(damage)
		if player and vampirism:
			player.take_heal(damage / 10)
	time += 1
	if time >= lifetime:
		if get_parent().is_in_group("enemy"):
			get_parent().speed_multiplier += slowdown_var
		queue_free()
