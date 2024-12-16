extends CharacterBody2D
class_name Ghost

enum State{
	KNOCKBACK,
	WAIT,
	TURN_OFF,
}
var state = State.TURN_OFF

const SPEED = 1000.0
const KNOCKBACK_RANGE := 400
var remaining_knockback_range := 0

var knockback_ready = true

var player : Node




func turn_off():
	state = State.TURN_OFF

func turn_on():
	state = State.WAIT
	knockback_ready = true

func _ready():
	if get_node("/root/EndlessCorridor/Character"):
		player = get_node("/root/EndlessCorridor/Character")
	else: # player == null:
		player = get_node("/root/EndRoom/Character")
		await get_tree().create_timer(3).timeout 
		state = State.WAIT


func get_vector_to_player():
	if player:
		return (player.position - position).normalized()
	else:
		return Vector2.ZERO

func _physics_process(delta):
	match state:
		State.TURN_OFF:
			pass
		State.WAIT:
			start_knockback()
		State.KNOCKBACK:
			knockback(delta)

func start_knockback():
	if knockback_ready:
		knockback_ready = false
		state = State.KNOCKBACK
		velocity = get_vector_to_player() * SPEED
		remaining_knockback_range = KNOCKBACK_RANGE

func knockback(delta):
	move_and_slide()
	remaining_knockback_range -= SPEED * delta
	check_stop_knockback()

func check_stop_knockback():
	if remaining_knockback_range <= 0:
		stop_knockback()

func stop_knockback():
	state = State.WAIT
	knockback_ready = false
	await get_tree().create_timer(1).timeout
	knockback_ready = true


func _on_area_2d_body_entered(_body):
	player.dead()


