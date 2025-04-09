import math
import pygame


import settings as Settings
import game.level_manager as LevelManager

import game.object_class_manager as ObjectClassManager


import game.objects.dynamic_objects.entities.base_entity as BaseEntity
import game.objects.dynamic_objects.base_dynamic_object as BaseDynamicObject


VELOCITY_INERTIA_FACTOR: int = 4
BOBBING_AMPLITUDE: float = 1
BOBBING_SPEED: float = 0.1

def new(position: pygame.Vector2 = pygame.Vector2()) -> dict:
	return ObjectClassManager.new_object(BaseEntity.new(position), {
		"groups": {"Player"},
		"class": "Player",

		"collision_layer": Settings.PLAYER,
		"collision_mask": Settings.WALL | Settings.OBSTACLE | Settings.ENEMY,
		"rotation": 0.0,

		"speed": 128,
		"bobbing_timer": 0,

		"max_health": 100,
		"health": 100,

		"height": 32,
	})


def update(self: dict, delta: float) -> None:
	move(self, delta)
	rotate(self)
	bobbing(self, delta)

def move(self: dict, delta: float) -> None:
	keys = pygame.key.get_pressed()
	input_direction: pygame.Vector2 = pygame.Vector2(keys[Settings.move_right] - keys[Settings.move_left], keys[Settings.move_backward] - keys[Settings.move_forward])

	move_direction: pygame.Vector2 = pygame.Vector2()
	if input_direction.x != 0 or input_direction.y != 0: move_direction = input_direction.rotate_rad(self["rotation"] + Settings.HALF_PI).normalize()

	self["velocity"] = self["velocity"].lerp(move_direction * self["speed"], min(delta * VELOCITY_INERTIA_FACTOR, 1))
	BaseDynamicObject.move_and_slide(self, delta)


def rotate(self: dict) -> None:
	rel_x: int = pygame.mouse.get_rel()[0]
	yaw: float = (rel_x / Settings.resolution[0] / 4) * Settings.fov_h * Settings.camera_sensitivity
	self["rotation"] = (self["rotation"] + yaw) % math.tau


def bobbing(self: dict, delta: float) -> None:
	bob_timer = (self["bobbing_timer"] + self["velocity"].length() * BOBBING_SPEED * delta) % math.tau
	self["bobbing_timer"] = bob_timer
	self["position_z"] = math.sin(bob_timer) * BOBBING_AMPLITUDE



def die(self: dict) -> None:
	self["dead"] = True
	LevelManager.load_level()
	self["health"] = self["max_health"]
	self["dead"] = False
