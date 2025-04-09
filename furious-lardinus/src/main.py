# Pavlov Aleksandr s2400691
# lardinois joachim s2402075
# Gendebien Alexandre s2404939


import sys
import pygame


import settings as Settings
import core.events as Events
import main_state_machine as StateMachine


clock: pygame.time.Clock


def main() -> None:
	init()
	run()


def init() -> None:
	global clock
	pygame.init()
	pygame.display.set_mode(Settings.resolution, pygame.SCALED)
	pygame.display.set_caption(Settings.NAME)
	clock = pygame.time.Clock()
	StateMachine.init()


def run() -> None:
	while True:
		update()
		Events.update()
		check_events()
		StateMachine.update(clock.get_time() / 1000)
		pygame.display.set_caption(str(int(clock.get_fps())))


def update():
	clock.tick(Settings.tick_fps)
	Settings.current_fps = clock.get_fps()


def check_events() -> None:
	for event in Events.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == Settings.full_screen:
				pygame.display.toggle_fullscreen()


if __name__ == "__main__":
	main()
