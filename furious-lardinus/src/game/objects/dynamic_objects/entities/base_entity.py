import pygame


import game.object_class_manager as ObjectClassManager
import game.object_manager as ObjectManager


import game.objects.dynamic_objects.base_dynamic_object as BaseDynamicObject


def new(position: pygame.Vector2 = pygame.Vector2()) -> dict:
	return ObjectClassManager.new_object(BaseDynamicObject.new(position), {
		"groups": {"Entity"},
		"class": "BaseEntity",

		"collidable": True,

		"speed": 64,

		"max_health": 100,
		"health": 100,
		"dead": False,
	})


def take_damage(self: dict, damage: int) -> None:
	if damage <= 0: return
	new_health: int = int(pygame.math.clamp(self["health"] - damage, 0, self["max_health"]))
	self["health"] = new_health
	if new_health == 0: ObjectClassManager.die(self)


def take_heal(self: dict, heal: int) -> None:
	if heal <= 0: return
	self["health"] = pygame.math.clamp(self["health"] + heal, 0, self["max_health"])


def die(self: dict) -> None:
	self["dead"] = True
	ObjectManager.remove_object(self)
