import pygame


# BaseObject
import game.objects.base_object as BaseObject
	# BaseActiveObject
import game.objects.active_objects.base_active_object as BaseActiveObject
		# Ammo
import game.objects.active_objects.ammo as Ammo
		# Medikit
import game.objects.active_objects.medikit as Medikit
		# Exit
import game.objects.active_objects.exit as Exit
	# BaseDynamicObject
import game.objects.dynamic_objects.base_dynamic_object as BaseDynamicObject
		# BaseEntity
import game.objects.dynamic_objects.entities.base_entity as BaseEntity
			# Player
import game.objects.dynamic_objects.entities.player as Player
			# BaseEnemy
import game.objects.dynamic_objects.entities.enemies.base_enemy as BaseEnemy
				# Knight
import game.objects.dynamic_objects.entities.enemies.knight as Knight
				# Summoner
import game.objects.dynamic_objects.entities.enemies.summoner as Summoner
				# Skull
import game.objects.dynamic_objects.entities.enemies.skull as Skull
				# Wizzard
import game.objects.dynamic_objects.entities.enemies.wizzard as Wizzard
import game.objects.dynamic_objects.entities.enemies.boss as Boss

		# BaseProjectile
import game.objects.dynamic_objects.projectiles.base_projectile as BaseProjectile
			# PlayerProjectile
import game.objects.dynamic_objects.projectiles.player_projectile as PlayerProjectile
			# WizzardProjectile
import game.objects.dynamic_objects.projectiles.wizzard_projectile as WizzardProjectile


def new_object(parent_object: dict, new_data: dict) -> dict:
	new_object: dict = parent_object | new_data
	new_groups: set | None = new_data.get("groups")
	if new_groups is not None: new_object["groups"] = parent_object["groups"] | new_groups
	return new_object


def update(self: dict, delta: float) -> None:
	groups: set = self["groups"]
	if "Player" in groups:
		Player.update(self, delta)
	elif "Enemy" in groups:
		BaseEnemy.update(self, delta)
	elif "Projectile" in groups:
		BaseProjectile.update(self, delta)


def object_collided(self: dict, game_object: dict) -> None:
	groups: set = self["groups"]
	object_class: set = self["class"]
	if "ActiveObject" in groups:
		if object_class == "Ammo": Ammo.object_collided(self, game_object)
		elif object_class == "Medikit": Medikit.object_collided(self, game_object)
		elif object_class == "Exit": Exit.object_collided(self, game_object)
	elif "Enemy" in groups:
		if object_class == "Skull": Skull.object_collided(self, game_object)
	elif "Projectile":
		if object_class == "PlayerProjectile": PlayerProjectile.object_collided(self, game_object)
		elif object_class == "WizzardProjectile": WizzardProjectile.object_collided(self, game_object)


def attack(self: dict) -> None:
	groups: set = self["groups"]
	object_class: set = self["class"]
	if "Enemy" in groups:
		if object_class == "Knight": Knight.attack(self)
		elif object_class == "Summoner": Summoner.attack(self)
		elif object_class == "Wizzard": Wizzard.attack(self)
		elif object_class == "Boss": Boss.attack(self)


def die(self: dict) -> None:
	groups: set = self["groups"]
	if "Player" in groups:
		Player.die(self)
	elif "Enemy" in groups:
		BaseEnemy.die(self)


def create_loot(self: dict) -> None:
	groups: set = self["groups"]
	object_class: set = self["class"]
	if "Enemy" in groups:
		if object_class == "Knight": Knight.create_loot(self)
		elif object_class == "Summoner": Summoner.create_loot(self)
		elif object_class == "Wizzard": Wizzard.create_loot(self)
		elif object_class == "Boss": Boss.create_loot(self)
