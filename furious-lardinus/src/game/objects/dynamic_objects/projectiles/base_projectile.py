import pygame


import settings as Settings


import game.object_class_manager as ObjectClassManager
import game.object_manager as ObjectManager


import game.objects.dynamic_objects.base_dynamic_object as BaseDynamicObject


def new(damage: int, position: pygame.Vector2 = pygame.Vector2(), velocity: pygame.Vector2 = pygame.Vector2()) -> dict:
	return ObjectClassManager.new_object(BaseDynamicObject.new(position, velocity), {
		"groups": {"Projectile"},
		"class": "BaseProjectile",

		"collision_layer": Settings.PROJECTILE,
		"collidable": False,

		"radius": 4,

		"position_z": -22.0,
		"height": 8,

		"damage": damage
	})


def update(self: dict, delta: float) -> None:
	BaseDynamicObject.move_and_slide(self, delta)
