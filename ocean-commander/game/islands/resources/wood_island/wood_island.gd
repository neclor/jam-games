extends Island


func work_complete():
	match side:
		Sides.PLAYER:
			Signals.player_got_wood.emit(product_amount * num_workers)
		Sides.ENEMY:
			Signals.enemy_got_wood.emit(product_amount * num_workers)
