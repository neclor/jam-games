extends Node


@warning_ignore("unused_signal")
signal pause_game
@warning_ignore("unused_signal")
signal resume_game
@warning_ignore("unused_signal")
signal game_over
@warning_ignore("unused_signal")
signal win


@warning_ignore("unused_signal")
signal enemy_ship_died
@warning_ignore("unused_signal")
signal player_ship_died

@warning_ignore("unused_signal")
signal enemy_selected(enemy: Node)

@warning_ignore("unused_signal")
signal player_got_gold(amount: int)
@warning_ignore("unused_signal")
signal player_got_wood(amount: int)
@warning_ignore("unused_signal")
signal enemy_got_gold(amount: int)
@warning_ignore("unused_signal")
signal enemy_got_wood(amount: int)


@warning_ignore("unused_signal")
signal enemy_boat_apeared(boat)

@warning_ignore("unused_signal")
signal enemy_warship_apeared(boat)



@warning_ignore("unused_signal")
signal restart_game

@warning_ignore("unused_signal")
signal color_changed(color: Color)
