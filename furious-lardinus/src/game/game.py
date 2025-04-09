import sys
import math
import pygame


import settings as Settings
import core.events as Events


import game.object_manager as ObjectManager
import game.level_manager as LevelManager
import game.rendering.display as Display
import game.objects.dynamic_objects.entities.player as Player
import game.weapon as Weapon


timer: float
pause: bool


player: dict


def enter() -> None:
	global timer, pause
	timer = 0.0
	pause = False
	mouse_visible(False)
	Display.init()

	start_game()


def toggle_pause() -> None:
	global pause
	pause = not pause
	mouse_visible(pause)


def mouse_visible(visible: bool) -> None:
	pygame.mouse.set_visible(visible)
	pygame.event.set_grab(not visible)


def start_game() -> None:
	global player
	player = Player.new()
	LevelManager.load_level()


def game_over() -> None:
	LevelManager.load_level()
	player["dead"] = False
	player["health"] = player["max_health"]


def update(delta: float) -> None:
	global timer
	if not pause:
		timer += delta
		Weapon.update(delta)
		ObjectManager.update(delta)
	Display.update()
	check_events()


def check_events() -> None:
	for event in Events.get():
		if event.type == pygame.KEYDOWN:
			if event.key == Settings.pause:
				toggle_pause()



def exit() -> None:
	pass
