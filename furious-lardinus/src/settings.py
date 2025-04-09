import math
import pygame


# Config
NAME: str = "Furious Lardinus"


# Dispaly
resolution: tuple[int, int] = (2 * 640, 2 * 360)
fps: int = 60


# Game settings
camera_sensitivity: float = 1.0
fov_h: float = math.tau / 3


# Input
full_screen: int = pygame.K_F11
pause: int = pygame.K_ESCAPE

move_forward: int = pygame.K_w
move_backward: int = pygame.K_s
move_left: int = pygame.K_a
move_right: int = pygame.K_d

gun: int = pygame.K_1
shotgun: int = pygame.K_2
assault: int = pygame.K_3


# Advanced
MIN_FOV_H: float = math.pi / 3
MAX_FOV_H: float = math.tau / 3
fps_amplitude: int = 20
current_fps: float = fps


# Collision layers
WALL: int = 1
OBSTACLE: int = 2
ACTIVE: int = 4
ENEMY: int = 8
PLAYER: int = 16
PROJECTILE: int = 32


# Calculated parameters
half_resolution: tuple[int, int]
aspect_ratio: float

max_fps_limit: int
tick_fps: int

fov_v: float
half_fov_h: float
half_fov_v: float

tan_half_fov_h: float
tan_half_fov_v: float
double_tan_half_fov_h: float
double_tan_half_fov_v: float

resolution_x_div_double_tan_half_fov_h: float
resolution_y_div_double_tan_half_fov_v: float


# Math
HALF_PI: float = math.pi / 2
THREE_HALF_PI: float = 3 * HALF_PI


def calculate_resolution_parameters() -> None:
	global half_resolution, aspect_ratio
	half_resolution = (resolution[0] // 2, resolution[1] // 2)
	aspect_ratio = resolution[0] / resolution[1]
	calculate_fov_parameters()


def calculate_fov_parameters() -> None:
	global fov_h, fov_v, half_fov_h, half_fov_v, tan_half_fov_h, tan_half_fov_v, double_tan_half_fov_h, double_tan_half_fov_v, resolution_x_div_double_tan_half_fov_h, resolution_y_div_double_tan_half_fov_v
	fov_h = pygame.math.clamp(fov_h, MIN_FOV_H, MAX_FOV_H)
	fov_v = 2 * math.atan(math.tan(fov_h / 2) / aspect_ratio)
	half_fov_h = fov_h / 2
	half_fov_v = fov_v / 2

	tan_half_fov_h = math.tan(half_fov_h)
	tan_half_fov_v = math.tan(half_fov_v)
	double_tan_half_fov_h = tan_half_fov_h * 2
	double_tan_half_fov_v = tan_half_fov_v * 2
	resolution_x_div_double_tan_half_fov_h = resolution[0] / double_tan_half_fov_h
	resolution_y_div_double_tan_half_fov_v = resolution[1] / double_tan_half_fov_v


def calculate_fps_parameters() -> None:
	global max_fps_limit, tick_fps
	max_fps_limit = fps + fps_amplitude
	tick_fps = fps + 2 * fps_amplitude


calculate_resolution_parameters()
calculate_fps_parameters()
