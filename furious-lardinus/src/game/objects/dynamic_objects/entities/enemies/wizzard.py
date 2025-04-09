import random
import pygame


import game.game as Game


import game.object_class_manager as ObjectClassManager
import game.object_manager as ObjectManager


import game.objects.dynamic_objects.entities.base_entity as BaseEntity
import game.objects.dynamic_objects.entities.enemies.base_enemy as BaseEnemy


import game.objects.dynamic_objects.projectiles.wizzard_projectile as WizzardProjectile


import game.objects.active_objects.ammo as Ammo


WIZZARD_SPRITE: pygame.Surface = pygame.image.load("src/assets/sprites/enemies/wizzard_32_48.png")
WIZZARD_PROJECTILE_SPEED: int = 192


def new(position: pygame.Vector2 = pygame.Vector2()) -> dict:
	return ObjectClassManager.new_object(BaseEnemy.new(position), {
		"class": "Wizzard",

		"position_z": 0.0,
		"height": 48,

		"sprite": WIZZARD_SPRITE,

		"speed": 32,

		"max_health": 100,
		"health": 100,

		"attack_cooldown": 2,
		"attack_range": 1024,
		"damage": 10,
	})


def attack(self: dict) -> None:
	position: pygame.Vector2 = self["position"]
	vector_to_player: pygame.Vector2 = Game.player["position"] - position
	distance: float = vector_to_player.length()
	if distance > 0:
		ObjectManager.add_object(WizzardProjectile.new(self["damage"], position.copy(), vector_to_player.normalize() * WIZZARD_PROJECTILE_SPEED))


def create_loot(self: dict) -> None:
	if random.randint(0, 2) == 0: pass
	ObjectManager.add_object(Ammo.new(self["position"].copy()))
