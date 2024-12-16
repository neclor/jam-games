extends Camera2D


const MAX_ZOOM = Vector2(2, 2)
const MIN_ZOOM = Vector2(0.75, 0.75)


func _ready():
	Global.camera = self


func zoom_in() -> void:
	if zoom < MAX_ZOOM:
		zoom *= 1.1


func zoom_out() -> void:
	if zoom > MIN_ZOOM:
		zoom /= 1.1


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("zoom_in"):
		zoom_in()
	elif event.is_action_pressed("zoom_out"):
		zoom_out()

	if event is InputEventScreenDrag:
		global_position -= event.relative / zoom
		global_position.x = clamp(global_position.x, limit_left + get_viewport_rect().size.x/2/zoom.x, limit_right - get_viewport_rect().size.x/2/zoom.x)
		global_position.y = clamp(global_position.y, limit_top + get_viewport_rect().size.y/2/zoom.x, limit_bottom - get_viewport_rect().size.y/2/zoom.x)
