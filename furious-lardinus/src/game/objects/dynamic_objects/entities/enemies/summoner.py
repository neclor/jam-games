import random
import pygame


import game.object_class_manager as ObjectClassManager
import game.object_manager as ObjectManager


import game.objects.dynamic_objects.entities.enemies.base_enemy as BaseEnemy
import game.objects.dynamic_objects.entities.enemies.skull as Skull


import game.objects.active_objects.ammo as Ammo


SUMMONER_SPRITE: pygame.Surface = pygame.image.load("src/assets/sprites/enemies/summoner_32_48.png")


def new(position: pygame.Vector2 = pygame.Vector2()) -> dict:
	return ObjectClassManager.new_object(BaseEnemy.new(position), {
		"class": "Summoner",

		"position_z": 0.0,
		"height": 48,

		"sprite": SUMMONER_SPRITE,

		"speed": 32,

		"max_health": 100,
		"health": 100,

		"attack_cooldown": 5,
		"attack_range": 1024,
	})


def attack(self: dict) -> None:
	ObjectManager.add_object(Skull.new(self["position"].copy()))


def create_loot(self: dict) -> None:
	if random.randint(0, 2) == 0: pass
	ObjectManager.add_object(Ammo.new(self["position"].copy()))
