import pygame


import settings as Settings


import game.object_class_manager as ObjectClassManager
import game.object_manager as ObjectManager


import game.objects.base_object as BaseObject


def new(position: pygame.Vector2 = pygame.Vector2()) -> dict:
	return ObjectClassManager.new_object(BaseObject.new(position), {
		"groups": {"ActiveObject"},
		"class": "BaseActiveObject",

		"collision_layer": Settings.ACTIVE,
		"collision_mask": Settings.PLAYER,

		"radius": 12,

		"position_z": 0.0,
		"height": 24,
	})
