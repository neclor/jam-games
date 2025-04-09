import pygame


import settings as Settings


import game.object_class_manager as ObjectClassManager
import game.object_manager as ObjectManager


import game.objects.dynamic_objects.projectiles.base_projectile as BaseProjectile
import game.objects.dynamic_objects.entities.base_entity as BaseEntity


PLAYER_PROJECTILE_SPRITE: pygame.Surface = pygame.image.load("src/assets/sprites/projectiles/player_projectile_8.png")


def new(damage: int, position: pygame.Vector2 = pygame.Vector2(), velocity: pygame.Vector2 = pygame.Vector2()) -> dict:
	return ObjectClassManager.new_object(BaseProjectile.new(damage, position, velocity), {
		"class": "PlayerProjectile",

		"collision_mask": Settings.WALL | Settings.ENEMY,
		"sprite": PLAYER_PROJECTILE_SPRITE,
	})


def object_collided(self: dict, game_object: dict) -> None:
	groups: set = game_object["groups"]
	if "Tile" in groups:
		ObjectManager.remove_object(self)
	elif "Enemy" in groups:
		BaseEntity.take_damage(game_object, self["damage"])
		ObjectManager.remove_object(self)
