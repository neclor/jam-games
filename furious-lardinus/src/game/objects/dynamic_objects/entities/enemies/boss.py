import random
import pygame


import game.game as Game


import game.object_class_manager as ObjectClassManager
import game.object_manager as ObjectManager


import game.objects.dynamic_objects.entities.base_entity as BaseEntity
import game.objects.dynamic_objects.entities.enemies.base_enemy as BaseEnemy


import game.objects.active_objects.ammo as Ammo
import game.objects.active_objects.medikit as Medikit
import game.objects.dynamic_objects.entities.enemies.skull as Skull

BOSS_SPRITE: pygame.Surface = pygame.image.load("src/assets/sprites/enemies/boss_128.png")


def new(position: pygame.Vector2 = pygame.Vector2()) -> dict:
	return ObjectClassManager.new_object(BaseEnemy.new(position), {
		"class": "Boss",

		"position_z": 0.0,
		"height": 128,

		"sprite": BOSS_SPRITE,

		"speed": 96,

		"max_health": 500,
		"health": 500,

		"attack_cooldown": 2,
		"attack_range": 128,
		"damage": 20,
	})


def attack(self: dict) -> None:
	BaseEntity.take_damage(Game.player, self["damage"])
	ObjectManager.add_object(Skull.new(self["position"].copy()))


def create_loot(self: dict) -> None:
	ObjectManager.add_object(Medikit.new(self["position"].copy()))
	ObjectManager.add_object(Ammo.new(self["position"].copy()))
	ObjectManager.add_object(Skull.new(self["position"].copy()))
