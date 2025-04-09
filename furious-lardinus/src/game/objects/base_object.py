import pygame


def new(position: pygame.Vector2 = pygame.Vector2()) -> dict:
	return {
		"freed": False,

		"groups": {"Object"},
		"class": "BaseObject",

		"collision_layer": 0,
		"collision_mask": 0,
		"collidable": False,
		"static": True,

		"position": position,
		"radius": 16,

		"position_z": 0.0,
		"height": 32,

		"sprite": None,
	}
