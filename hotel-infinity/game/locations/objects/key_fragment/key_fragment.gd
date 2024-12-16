extends Node2D
@onready var area_2d = $Area2D

var is_work : bool

func _ready():
	off()

func _on_body_entered(body):
	body.key_number += 1
	off()
	Sfx.play_collect()

func _physics_process(_delta):
	if !is_work:
		area_2d.monitoring = false

func on():
	self.visible = true
	is_work = true
	area_2d.monitoring = true

func off():
	self.visible = false
	is_work = false
	
