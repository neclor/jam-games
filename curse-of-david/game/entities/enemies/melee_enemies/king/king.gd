extends MeleeEnemy


func die():
	Signals.king_dead.emit()
	super.die()
