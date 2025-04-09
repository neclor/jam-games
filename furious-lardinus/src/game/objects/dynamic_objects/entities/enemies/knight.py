import random
import pygame


import game.game as Game


import game.object_class_manager as ObjectClassManager
import game.object_manager as ObjectManager


import game.objects.dynamic_objects.entities.base_entity as BaseEntity
import game.objects.dynamic_objects.entities.enemies.base_enemy as BaseEnemy


import game.objects.active_objects.medikit as Medikit


KNIGHT_SPRITE: pygame.Surface = pygame.image.load("src/assets/sprites/enemies/knight_32_48.png")


def new(position: pygame.Vector2 = pygame.Vector2()) -> dict:
	return ObjectClassManager.new_object(BaseEnemy.new(position), {
		"class": "Knight",

		"position_z": -16.0,
		"height": 48,

		"sprite": KNIGHT_SPRITE,

		"speed": 96,

		"max_health": 200,
		"health": 200,

		"attack_cooldown": 1,
		"attack_range": 32,
		"damage": 5,
	})


def attack(self: dict) -> None:
	BaseEntity.take_damage(Game.player, self["damage"])


def create_loot(self: dict) -> None:
	if random.randint(0, 2) == 0: pass
	ObjectManager.add_object(Medikit.new(self["position"].copy()))
