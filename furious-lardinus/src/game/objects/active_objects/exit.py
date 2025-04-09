import pygame


import game.object_class_manager as ObjectClassManager
import game.level_manager as LevelManager


import game.objects.active_objects.base_active_object as BaseActiveObject


EXIT_SPRITE: pygame.Surface = pygame.image.load("src/assets/sprites/objects/exit.png")

def new(position: pygame.Vector2 = pygame.Vector2()) -> dict:
	return ObjectClassManager.new_object(BaseActiveObject.new(position), {
		"class": "Exit",

		"radius": 16,

		"position_z": 0.0,
		"height": 64,
		"sprite": EXIT_SPRITE,
	})


def object_collided(self: dict, game_object: dict) -> None:
	groups: set = game_object["groups"]
	if "Player" in groups:
		LevelManager.next_level()
