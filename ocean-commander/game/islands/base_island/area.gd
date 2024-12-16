extends Node2D

const a = TAU / 26

func _draw():
	var angle: float = 0
	for i in 24:
		draw_arc(Vector2.ZERO, 256, angle, angle + a, 2, Color.GRAY, 16)
		angle += 2 * a
