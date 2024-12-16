class_name EnemyShip
extends Ship


func _ready() -> void:
	super()
	if max_hp < 200:
		Signals.enemy_boat_apeared.emit(self)
	else:
		Signals.enemy_warship_apeared.emit(self)


func _on_touch_screen_button_pressed() -> void:
	Global.ship_pressed = true
	Signals.enemy_selected.emit(self)


func _on_touch_screen_button_released() -> void:
	Global.ship_pressed = false


func die() -> void:
	if dead:
		return
	attack_timer.stop()
	Signals.enemy_ship_died.emit()
	dead = true
	damage_animation_player.play("death")
	await damage_animation_player.animation_finished
	queue_free()
