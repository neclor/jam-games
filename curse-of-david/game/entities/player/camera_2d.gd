extends Camera2D


const MAX_ZOOM = Vector2(2, 2)
const MIN_ZOOM = Vector2(0.25, 0.25)


func _input(event: InputEvent) -> void:
	if event.is_action_pressed("zoom_in"):
		zoom_in()

	elif event.is_action_pressed("zoom_out"):
		zoom_out()


func zoom_in() -> void:
	if zoom < MAX_ZOOM:
		zoom *= 1.1


func zoom_out() -> void:
	if zoom > MIN_ZOOM:
		zoom /= 1.1
