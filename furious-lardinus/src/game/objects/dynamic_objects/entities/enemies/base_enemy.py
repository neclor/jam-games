import pygame


import settings as Settings
import game.game as Game
import game.level_manager as LevelManager


import game.object_class_manager as ObjectClassManager
import game.object_manager as ObjectManager


import game.objects.dynamic_objects.base_dynamic_object as BaseDynamicObject
import game.objects.dynamic_objects.entities.base_entity as BaseEntity


def new(position: pygame.Vector2 = pygame.Vector2()) -> dict:
	return ObjectClassManager.new_object(BaseEntity.new(position), {
		"groups": {"Enemy"},
		"class": "BaseEnemy",

		"collision_layer": Settings.ENEMY,
		"collision_mask": Settings.WALL | Settings.OBSTACLE | Settings.ENEMY | Settings.PLAYER,

		"height": 48,

		"attack_cooldown": 1,
		"attack_cooldown_left": 0,
		"attack_range": 64,
		"damage": 10,
	})


def update(self: dict, delta: float) -> None:
	self["velocity"] = pygame.Vector2()
	update_cooldown(self, delta)
	if not see_player(self): return
	move_and_attack(self)
	BaseDynamicObject.move_and_slide(self, delta)


def update_cooldown(self: dict, delta: float) -> None:
	self["attack_cooldown_left"] = max(0, self["attack_cooldown_left"] - delta)


def move_and_attack(self: dict) -> None:
	vector_to_player: pygame.Vector2 = Game.player["position"] - self["position"]
	distance: float = vector_to_player.length()

	if distance > self["attack_range"] + Game.player["radius"]:
		self["velocity"] = vector_to_player.normalize() * self["speed"]
	elif self["attack_cooldown_left"] == 0:
		self["attack_cooldown_left"] = self["attack_cooldown"]
		ObjectClassManager.attack(self)


def see_player(self: dict) -> bool:
	position: pygame.Vector2 = self["position"]
	player_position: pygame.Vector2 = Game.player["position"]

	x: int = int(position.x // LevelManager.tile_size.x)
	y: int = int(position.y // LevelManager.tile_size.y)
	player_x: int = int(player_position.x // LevelManager.tile_size.x)
	player_y: int = int(player_position.y // LevelManager.tile_size.y)

	ray_sign_x: int = 1 if x < player_x else (-1 if x > player_x else 0)
	ray_sign_y: int = 1 if y < player_y else (-1 if y > player_y else 0)
	abs_delta_x: int = abs(x - player_x)
	abs_delta_y: int = abs(y - player_y)

	error: int = abs_delta_x - abs_delta_y
	while True:
		if not (0 <= x < LevelManager.tile_map_size.x and 0 <= y < LevelManager.tile_map_size.y): return False
		tile: dict | None = LevelManager.tile_map[y][x]
		if tile is not None and (tile["collision_layer"] & Settings.WALL > 0): return False

		if x == player_x and y == player_y: return True

		if error >= 0:
			error -= abs_delta_y
			x += ray_sign_x
		if error <= 0:
			error += abs_delta_x
			y += ray_sign_y


def die(self: dict) -> None:
	ObjectClassManager.create_loot(self)
	BaseEntity.die(self)
