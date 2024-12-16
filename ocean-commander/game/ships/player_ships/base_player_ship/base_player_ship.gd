class_name PlayerShip
extends Ship


var selected: bool = false


func _ready() -> void:
	super._ready()
	Signals.enemy_selected.connect(set_target)


func set_target(enemy: Node):
	if selected:
		selected = false
		queue_redraw()
		target = enemy


func _draw() -> void:
	if selected:
		draw_arc(Vector2(0, -24), 64, 0, TAU, 128, Color.WHITE, 8)


func _on_touch_screen_button_pressed() -> void:
	Global.ship_pressed = true
	selected = not selected
	queue_redraw()


func _on_touch_screen_button_released() -> void:
	Global.ship_pressed = false


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventScreenTouch and event.is_pressed():
		if Global.ship_pressed:
			return
		elif selected:
			target = null
			destination = true
			var pos = (Global.camera.global_position - Global.camera.get_viewport_rect().size/2/Global.camera.zoom.x)
			pos += event.position /Global.camera.zoom.x
			navigation_agent_2d.target_position = pos
			selected = false
			queue_redraw()


func die() -> void:
	if dead:
		return
	attack_timer.stop()
	Signals.player_ship_died.emit()
	dead = true
	damage_animation_player.play("death")
	await damage_animation_player.animation_finished
	queue_free()
