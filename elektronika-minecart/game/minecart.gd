extends Area2D

var main 

func _ready():
	main = get_parent()


func _on_body_entered(body):
	main.add_gold()
	body.queue_free()
