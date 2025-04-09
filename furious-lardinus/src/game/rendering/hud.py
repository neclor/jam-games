import pygame


import settings as Settings
import game.rendering.display as Display
import game.game as Game
import game.weapon as Weapon


WHITE: pygame.Color = pygame.Color("#ffffff")


font: pygame.font.Font


def init() -> None:
	global font
	font = pygame.font.Font("src/assets/fonts/Pixel_Game.otf", 64)


def update() -> None:
	timer_min: int = int(Game.timer // 60)
	timer_sec: int = int(Game.timer % 60)


	timer_surface = font.render(str(timer_min) + ":" + str(timer_sec), True, WHITE)
	timer_rect = timer_surface.get_rect(y = 0, centerx = Settings.half_resolution[0])


	hp_surface = font.render(str(Game.player["health"]), True, WHITE)
	hp_rect = hp_surface.get_rect(midbottom = (Settings.half_resolution[0], Settings.resolution[1]))


	weapon_surface = font.render(Weapon.current_weapon["name"], True, WHITE)
	weapon_rect = weapon_surface.get_rect(bottomleft = (0, Settings.resolution[1]))


	ammo_surface = font.render(str(Weapon.current_weapon["ammo"]), True, WHITE)
	ammo_rect = ammo_surface.get_rect(bottomright = Settings.resolution)


	Display.surface.blit(timer_surface, timer_rect)
	Display.surface.blit(hp_surface, hp_rect)
	Display.surface.blit(weapon_surface, weapon_rect)
	Display.surface.blit(ammo_surface, ammo_rect)
