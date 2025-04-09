import pygame


import game.rendering.renderer_3d as Renderer3D
import game.rendering.hud as HUD


surface: pygame.Surface


def init() -> None:
	global surface
	surface = pygame.display.get_surface()
	Renderer3D.init()
	HUD.init()


def update() -> None:
	surface.fill(pygame.Color(0, 0, 0))
	Renderer3D.update()
	HUD.update()
	pygame.display.flip()
