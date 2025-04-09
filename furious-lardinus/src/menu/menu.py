import pygame


import main_state_machine as StateMachine
import settings as Settings
import core.events as Events


MAIN_MENU: int = 0
MENU_SETTINGS: int = 1


button_action: list[int] = [] # index represents button position, int represents the actions to take in action()
surface: pygame.Surface
menu_images: dict
menu_state: int = MAIN_MENU
selected: int = 1
settings_temp: int = 0


def menu_enter() -> None:
	menu_init()


def menu_init() -> None:
	global surface, menu_images
	pygame.mouse.set_visible(True)
	pygame.event.set_grab(False)
	surface = pygame.display.get_surface()
	menu_images = menu_load_images()
	pygame.key.set_repeat(200, 200)


def menu_load_images() -> dict:
	images: dict = {}
	title_font = pygame.font.Font("src/assets/fonts/Pixel_Game.otf", 200)
	button_font = pygame.font.Font("src/assets/fonts/Pixel_Game.otf", 80)
	big_button_font = pygame.font.Font("src/assets/fonts/Pixel_Game.otf", 120)
	images['bg'] = pygame.image.load("src/assets/sprites/menu/BG.png")
	images['bg'] = pygame.transform.scale(images['bg'], Settings.resolution)
	images['title'] = title_font.render("furious lardinus", True, (0, 0, 0))
	images['settings'] = title_font.render("Settings", True, (0, 0, 0))
	images['play'] = button_font.render("Play", True, (255, 255, 255))
	images['playselected'] = big_button_font.render("Play", True, (0, 255, 0))
	images['settings'] = button_font.render("Settings", True, (255, 255, 255))
	images['settingsselected'] = big_button_font.render("Settings", True, (0, 255, 0))
	images['quit'] = button_font.render("quit", True, (255, 255, 255))
	images['quitselected'] = big_button_font.render("quit", True, (0, 255, 0))
	images['sound'] = button_font.render("Sound", True, (255, 255, 255))
	images['soundselected'] = big_button_font.render("Sound", True, (0, 255, 0))
	images['return'] = button_font.render("return", True, (255, 255, 255))
	images['returnselected'] = big_button_font.render("return", True, (0, 255, 0))
	return images


def menu_update(delta: float) -> None:
	menu_state_machine(menu_state)


def menu_draw(bg: tuple[str, tuple[int, int]], title: tuple[str, tuple[int, int]], buttons: list[tuple[str, tuple[int, int]]]):
	global surface
	menu_draw_image(bg)
	menu_draw_image(title)
	button_count = 0
	for button in buttons:
		if button_count == selected:
			menu_draw_image((button[0]+'selected', button[1]))
		else:
			menu_draw_image(button)
		button_count += 1
	pygame.display.update()


def menu_draw_image(image_info: tuple[str, tuple[int, int]]):
	global surface
	surface.blit(menu_images[image_info[0]], menu_position_image(image_info[1], menu_images[image_info[0]].get_size()))


def menu_position_image(position: tuple[int, int], dimensions: tuple[int, int]):
	return (position[0] - dimensions[0] / 2, position[1] - dimensions[1] / 2)


def menu_action(action: int) -> None:
	global menu_state
	match action:
		case 0: StateMachine.change_state(1) 						# play
		case 1: menu_state = MENU_SETTINGS 							# settings
		case 2: pygame.event.post(pygame.event.Event(pygame.QUIT))	# quit
		case 3: print("sound")										# sound
		case 4: menu_state = MAIN_MENU								# return to main menu
		case 5: menu_increase_temp()										# increase temporary variable for settings change
		case 6: menu_decrease_temp()										# decrease temporary variable for settings change


def menu_increase_temp() -> None:
	global settings_temp
	settings_temp += 1


def menu_decrease_temp() -> None:
	global settings_temp
	settings_temp -= 1


def menu_input(button_number: int) -> None:
	global selected
	events = Events.get()
	for event in events:
		if event.type == pygame.KEYDOWN:
			if event.key == Settings.move_forward:
				selected -= 1
			if event.key == Settings.move_backward:
				selected += 1
			if event.key == pygame.K_RETURN:
				menu_action(button_action[selected])
	selected = selected % button_number


def menu_state_machine(state: int) -> None:
	match state:
		case 0: menu_main()
		case 1: menu_settings()


def menu_main() -> None:
	global button_action
	button_action = [0, 1, 2]
	menu_input(3)
	bg = ('bg', Settings.half_resolution)
	title = ('title', (Settings.half_resolution[0], 200))
	buttons = [
		('play', (Settings.half_resolution[0], 400)),
		('settings', (Settings.half_resolution[0], 500)),
		('quit', (Settings.half_resolution[0], 600)),
	]
	menu_draw(bg, title, buttons)


def menu_settings() -> None:
	global button_action
	button_action = [3, 4]
	menu_input(2)
	bg = ('bg', Settings.half_resolution)
	title = ('settings', (Settings.half_resolution[0], 200))
	buttons = [
		('sound', (Settings.half_resolution[0], 400)),
		('return', (Settings.half_resolution[0], 500)),
	]
	menu_draw(bg, title, buttons)


def menu_exit() -> None:
	pass
