import pygame


import game.object_class_manager as ObjectClassManager
import game.object_manager as ObjectManager


import game.objects.active_objects.base_active_object as BaseActiveObject


import game.objects.dynamic_objects.entities.base_entity as BaseEntity


MEDIKIT_SPRITE: pygame.Surface = pygame.image.load("src/assets/sprites/objects/medikit_16.png")
HEAL_AMOUNT: int = 25


def new(position: pygame.Vector2 = pygame.Vector2()) -> dict:
	return ObjectClassManager.new_object(BaseActiveObject.new(position), {
		"class": "Medikit",

		"sprite": MEDIKIT_SPRITE,
	})


def object_collided(self: dict, game_object: dict) -> None:
	groups: set = game_object["groups"]
	if "Player" in groups and game_object["health"] < game_object["max_health"]:
		BaseEntity.take_heal(game_object, HEAL_AMOUNT)
		ObjectManager.remove_object(self)
