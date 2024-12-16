extends AudioStreamPlayer
const DOOR = preload("res://assets/sound/door.mp3")

const STEP = preload("res://assets/sound/step.mp3")
const SWITCH = preload("res://assets/sound/switch.mp3")
const COLLECT = preload("res://assets/sound/collect.mp3")

func play_switch():
	stream = SWITCH
	play()

func play_door():
	stream = DOOR
	play()

func play_collect():
	stream = COLLECT
	play()
