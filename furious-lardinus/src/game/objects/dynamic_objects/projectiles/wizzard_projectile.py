import pygame


import settings as Settings


import game.object_class_manager as ObjectClassManager
import game.object_manager as ObjectManager


import game.objects.dynamic_objects.projectiles.base_projectile as BaseProjectile
import game.objects.dynamic_objects.entities.base_entity as BaseEntity


WIZZARD_PROJECTILE_SPRITE: pygame.Surface = pygame.image.load("src/assets/sprites/projectiles/wizzard_projectile_16.png")


def new(damage: int, position: pygame.Vector2 = pygame.Vector2(), velocity: pygame.Vector2 = pygame.Vector2()) -> dict:
	return ObjectClassManager.new_object(BaseProjectile.new(damage, position, velocity), {
		"class": "WizzardProjectile",

		"collision_mask": Settings.WALL | Settings.PLAYER,

		"radius": 8,

		"position_z": -8.0,
		"height": 16,

		"sprite": WIZZARD_PROJECTILE_SPRITE,
	})


def object_collided(self: dict, game_object: dict) -> None:
	groups: set = game_object["groups"]
	if "Tile" in groups:
		ObjectManager.remove_object(self)
	elif "Player" in groups:
		BaseEntity.take_damage(game_object, self["damage"])
		ObjectManager.remove_object(self)
