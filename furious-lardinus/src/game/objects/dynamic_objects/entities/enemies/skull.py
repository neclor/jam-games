import random
import pygame


import settings as Settings
import game.game as Game


import game.object_class_manager as ObjectClassManager
import game.object_manager as ObjectManager


import game.objects.dynamic_objects.entities.base_entity as BaseEntity
import game.objects.dynamic_objects.entities.enemies.base_enemy as BaseEnemy


SKULL_SPRITE: pygame.Surface = pygame.image.load("src/assets/sprites/enemies/skull_32.png")


def new(position: pygame.Vector2 = pygame.Vector2()) -> dict:
	return ObjectClassManager.new_object(BaseEnemy.new(position), {
		"class": "Skull",

		"collision_layer": Settings.ENEMY,
		"collision_mask": Settings.WALL | Settings.PLAYER,
		"collidable": False,

		"position_z": -32.0,
		"height": 32,

		"sprite": SKULL_SPRITE,

		"speed": 128,

		"max_health": 50,
		"health": 50,

		"attack_range": 0,
		"damage": 5,
	})


def object_collided(self: dict, game_object: dict) -> None:
	groups: set = game_object["groups"]
	if "Tile" in groups:
		BaseEnemy.die(self)
	elif "Player" in groups:
		BaseEntity.take_damage(game_object, self["damage"])
		BaseEnemy.die(self)
