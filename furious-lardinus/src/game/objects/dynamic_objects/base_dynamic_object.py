import pygame


import game.object_class_manager as ObjectClassManager


import game.objects.base_object as BaseObject


def new(position: pygame.Vector2 = pygame.Vector2(), velocity: pygame.Vector2 = pygame.Vector2()) -> dict:
	return ObjectClassManager.new_object(BaseObject.new(position), {
		"groups": {"DynamicObject"},
		"class": "BaseDynamicObject",

		"static": False,

		"velocity": velocity,
	})


def move_and_slide(self: dict, delta: float) -> None:
	self["position"] += self["velocity"] * delta
