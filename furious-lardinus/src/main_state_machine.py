import pygame


import menu.menu as Menu
import game.game as Game


# States = {
MENU: int = 0
GAME: int = 1
# }
INITIAL_STATE: int = MENU
state: int = -1


def init() -> None:
	change_state(INITIAL_STATE)


def update(delta: float) -> None:
	match state:
		case 0: Menu.menu_update(delta)
		case 1: Game.update(delta)


def change_state(new_state: int) -> None:
	global state
	if (new_state == state) or not (0 <= new_state <= 1): return

	match state:
		case 0: Menu.menu_exit()
		case 1: Game.exit()

	state = new_state

	match new_state:
		case 0: Menu.menu_enter()
		case 1: Game.enter()
