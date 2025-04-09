import math
import random
import pygame


import settings as Settings
import core.events as Events


import game.game as Game
import game.object_manager as ObjectManager
import game.objects.dynamic_objects.projectiles.player_projectile as PlayerProjectile


PLAYER_PROJECTILE_SPEED: int = 320


gun: dict = {
	"name": "Gun",
	"available": True,
	"sprite": None,
	"damage": 20,
	"max_ammo": math.inf,
	"ammo": math.inf,
	"cooldown": 0.3,
}
shotgun: dict = {
	"name": "Shotgun",
	"available": True,
	"sprite": None,
	"damage": 30,
	"max_ammo": 100,
	"ammo": 100,
	"cooldown": 0.5,
}
assault: dict = {
	"name": "Assault Rifle",
	"available": True,
	"sprite": None,
	"damage": 15,
	"max_ammo": 200,
	"ammo": 200,
	"cooldown": 0.1,
}


current_weapon: dict = gun
cooldown_left: float = 0


def update(delta: float) -> None:
	update_cooldown(delta)
	check_events()

	if current_weapon is assault:
		if pygame.mouse.get_pressed()[0]:
			shoot()



def add_ammo(ammo: int) -> bool:
	ammo_recived = False
	if shotgun["available"] and shotgun["ammo"] < shotgun["max_ammo"]:
		shotgun["ammo"] = min(shotgun["ammo"] + ammo, shotgun["max_ammo"])
		ammo_recived = True
	if assault["available"] and assault["ammo"] < assault["max_ammo"]:
		assault["ammo"] = min(assault["ammo"] + ammo * 2, assault["max_ammo"])
		ammo_recived = True

	return ammo_recived


def update_cooldown(delta: float) -> None:
	global cooldown_left
	cooldown_left = max(cooldown_left - delta, 0)


def shoot() -> None:
	global cooldown_left
	if cooldown_left > 0: return
	if current_weapon["ammo"] <= 0: return
	current_weapon["ammo"] -= 1
	cooldown_left = current_weapon["cooldown"]
	if current_weapon is gun:
		gun_shoot()
	elif current_weapon is shotgun:
		shotgun_shot()
	else:
		assault_shot()


def gun_shoot() -> None:
	position: pygame.Vector2 = Game.player["position"]
	velocity: pygame.Vector2 = pygame.Vector2(PLAYER_PROJECTILE_SPEED, 0).rotate_rad(Game.player["rotation"])
	ObjectManager.add_object(PlayerProjectile.new(current_weapon["damage"], position.copy(), velocity))


def shotgun_shot() -> None:
	position: pygame.Vector2 = Game.player["position"]
	velocity: pygame.Vector2 = pygame.Vector2(PLAYER_PROJECTILE_SPEED, 0).rotate_rad(Game.player["rotation"])
	for i in range(5):
		ObjectManager.add_object(PlayerProjectile.new(current_weapon["damage"], position.copy(), velocity.rotate_rad(random.uniform(-Settings.HALF_PI / 4, Settings.HALF_PI / 4))))


def assault_shot() -> None:
	position: pygame.Vector2 = Game.player["position"]
	velocity: pygame.Vector2 = pygame.Vector2(PLAYER_PROJECTILE_SPEED, 0).rotate_rad(Game.player["rotation"] + random.uniform(-0.1, 0.1))
	ObjectManager.add_object(PlayerProjectile.new(current_weapon["damage"], position.copy(), velocity))


def change_weapon(new_weapon: dict) -> None:
	global current_weapon, cooldown_left
	if current_weapon is new_weapon: return
	if not new_weapon["available"]: return
	current_weapon = new_weapon
	cooldown_left = current_weapon["cooldown"]


def check_events() -> None:
	for event in Events.get():
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			shoot()
		elif event.type == pygame.KEYDOWN:
			match event.key:
				case Settings.gun:
					change_weapon(gun)
				case Settings.shotgun:
					change_weapon(shotgun)
				case Settings.assault:
					change_weapon(assault)
