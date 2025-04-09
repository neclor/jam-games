import pygame


import game.object_class_manager as ObjectClassManager
import game.object_manager as ObjectManager

import game.objects.active_objects.base_active_object as BaseActiveObject
import game.objects.base_object as BaseObject


import game.weapon as Weapon

AMMO_SPRITE: pygame.Surface = pygame.image.load("src/assets/sprites/objects/ammo_16.png")
AMMO_AMOUNT: int = 25


def new(position: pygame.Vector2 = pygame.Vector2()) -> dict:
	return ObjectClassManager.new_object(BaseActiveObject.new(position), {
		"class": "Ammo",

		"sprite": AMMO_SPRITE,
	})


def object_collided(self: dict, game_object: dict) -> None:
	groups: set = game_object["groups"]
	if "Player" in groups:
		if Weapon.add_ammo(AMMO_AMOUNT): ObjectManager.remove_object(self)
