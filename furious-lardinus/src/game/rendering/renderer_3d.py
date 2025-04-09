import math
import pygame

import settings as Settings
import game.rendering.display as Display
import game.game as Game
import game.object_manager as ObjectManager
import game.level_manager as LevelManager


MIN_RAY_COUNT: int = 64
MAX_RAY_COUNT: int = 640
ray_count: int
ray_step_angle: float
ray_step_angle_tan: float
adjust_ray_counter: int


position: pygame.Vector2
rotation: float
rotation_tan: float
camera_position_z: float


def init() -> None:
	global ray_count, adjust_ray_counter
	ray_count = (MAX_RAY_COUNT - MIN_RAY_COUNT) // 2
	adjust_ray_counter = 0
	update_ray_parameters()


def update() -> None:
	adjust_ray_number()
	update_camera()
	draw_floor()
	draw_game()


def draw_floor() -> None:
	pygame.draw.rect(Display.surface, LevelManager.floor_color, (0, Settings.half_resolution[1], Settings.resolution[0], Settings.half_resolution[1]))


def adjust_ray_number() -> None:
	global adjust_ray_counter
	adjust_ray_counter += 1
	if adjust_ray_counter < 10: return
	adjust_ray_counter = 0

	global ray_count
	if Settings.current_fps < Settings.fps and ray_count > MIN_RAY_COUNT:
		ray_count -= 8
	elif Settings.current_fps > Settings.max_fps_limit and ray_count < MAX_RAY_COUNT:
		ray_count += 8
	else: return
	update_ray_parameters()


def update_ray_parameters():
	global ray_step_angle, ray_step_angle_tan
	ray_step_angle = Settings.fov_h / ray_count
	ray_step_angle_tan = math.tan(ray_step_angle)


def update_camera() -> None:
	global position, rotation, rotation_tan, camera_position_z
	position = Game.player["position"]
	rotation = Game.player["rotation"]
	rotation_tan = math.tan(rotation)
	camera_position_z = Game.player["position_z"] - Game.player["height"]


def draw_game() -> None:
	projections: list[tuple[pygame.Surface, pygame.Vector2, float]] = []
	projections += get_object_projections() + get_tile_map_projections()
	projections.sort(key = lambda a: a[2], reverse = True)
	for projection in projections:
		Display.surface.blit(projection[0], projection[1])


def get_object_projections() -> list[tuple[pygame.Surface, pygame.Vector2, float]]:
	object_projections: list[tuple[pygame.Surface, pygame.Vector2, float]] = []

	for game_object in ObjectManager.game_objects:
		object_projection: tuple[pygame.Surface, pygame.Vector2, float] | None = get_object_projection(game_object)
		if object_projection is not None: object_projections.append(object_projection)

	return object_projections


def get_object_projection(game_object: dict) -> tuple[pygame.Surface, pygame.Vector2, float] | None:
	object_radius: int = game_object["radius"]

	relative_object_position: pygame.Vector2 = pygame.Vector2(game_object["position"] - position).rotate_rad(-rotation - Settings.HALF_PI)
	relative_object_position.y *= -1

	if relative_object_position.y <= 1: return None

	tan_left_relative_angle: float = (relative_object_position.x - object_radius) / relative_object_position.y
	tan_right_relative_angle: float = (relative_object_position.x + object_radius) / relative_object_position.y
	if object_out_of_view(tan_left_relative_angle, tan_right_relative_angle): return None

	relative_object_bottom: float = game_object["position_z"] - camera_position_z
	relative_object_top: float = relative_object_bottom - game_object["height"]

	return calculate_projection(tan_left_relative_angle, tan_right_relative_angle, relative_object_position.y, relative_object_top, relative_object_bottom, game_object["sprite"])


def object_out_of_view(tan_left_relative_angle: float, tan_right_relative_angle: float) -> bool:
	return (
		max(tan_left_relative_angle, tan_right_relative_angle) <= -Settings.tan_half_fov_h or
		min(tan_left_relative_angle, tan_right_relative_angle) >= Settings.tan_half_fov_h)


def get_tile_map_projections() -> list[tuple[pygame.Surface, pygame.Vector2, float]]:
	tile_projections: list[tuple[pygame.Surface, pygame.Vector2, float]] = []

	ray_rotation: float = rotation - Settings.half_fov_h
	for _ in range(ray_count):
		tile_projections += cast_ray(ray_rotation)
		ray_rotation += ray_step_angle

	return tile_projections


def cast_ray(ray_rotation: float) -> list[tuple[pygame.Surface, pygame.Vector2, float]]:
	tile_projections: list[tuple[pygame.Surface, pygame.Vector2, float]] = []

	ray_relative_angle: float = ray_rotation - rotation
	ray_rotation = ray_rotation % math.tau
	ray_sign: pygame.Vector2 = pygame.Vector2((Settings.THREE_HALF_PI < ray_rotation <= math.tau or 0 <= ray_rotation < Settings.HALF_PI) - (Settings.HALF_PI < ray_rotation < Settings.THREE_HALF_PI), (0 < ray_rotation < math.pi) - (math.pi < ray_rotation < math.tau))
	signed_tile_size: pygame.Vector2 = pygame.Vector2(ray_sign.x * LevelManager.tile_size.x, ray_sign.y * LevelManager.tile_size.y)

	ray_tan: float = math.tan(ray_rotation)
	abs_ray_tan: float = abs(ray_tan)
	ray_relative_angle_cos: float = math.cos(ray_relative_angle)
	ray_relative_angle_tan: float = (ray_tan - rotation_tan) / (1 + ray_tan * rotation_tan)
	right_ray_relative_angle_tan: float = (ray_relative_angle_tan + ray_step_angle_tan) / (1 - ray_relative_angle_tan * ray_step_angle_tan)

	ray_position: pygame.Vector2 = position

	tile_index_x_whole, tile_index_x_fractional = divmod(ray_position.x, LevelManager.tile_size.x)
	tile_index_y_whole, tile_index_y_fractional = divmod(ray_position.y, LevelManager.tile_size.y)
	tile_index: pygame.Vector2 = pygame.Vector2(
		tile_index_x_whole - (ray_sign.x < 0 and tile_index_x_fractional == 0),
		tile_index_y_whole - (ray_sign.y < 0 and tile_index_y_fractional == 0))
	next_line: pygame.Vector2 = pygame.Vector2(
		(tile_index.x + (0 <= ray_sign.x)) * LevelManager.tile_size.x,
		(tile_index.y + (0 <= ray_sign.y)) * LevelManager.tile_size.y)

	#previous_tile: dict | None = None #TODO add drawing transparent tiles backside

	tan_min_obscured_angle: float = Settings.tan_half_fov_v
	tan_max_obscured_angle: float = -1 * Settings.tan_half_fov_v
	while not line_out_of_bounds(ray_sign, tile_index):
		delta_next_line: pygame.Vector2 = next_line - ray_position
		delta_ratio: float = delta_next_line.y / delta_next_line.x if delta_next_line.x != 0 else math.inf
		tan_delta_difference: float = abs_ray_tan - abs(delta_ratio)
		if tan_delta_difference < 0:
			ray_position = pygame.Vector2(next_line.x, position.y + (next_line.x - position.x) * ray_tan)
			next_line.x += signed_tile_size.x
			tile_index.x += ray_sign.x
		elif 0 < tan_delta_difference:
			ray_position = pygame.Vector2(position.x + (next_line.y - position.y) / ray_tan, next_line.y)
			next_line.y += signed_tile_size.y
			tile_index.y += ray_sign.y
		else:
			ray_position = pygame.Vector2(next_line.x, next_line.y)
			next_line += signed_tile_size
			tile_index += ray_sign

		ray_vector: pygame.Vector2 = ray_position - position
		distance: float = ray_vector.length()

		relative_min_obscured_point: float = distance * tan_min_obscured_angle
		relative_max_obscured_point: float = distance * tan_max_obscured_angle
		if relative_min_obscured_point <= LevelManager.min_point_z - camera_position_z and LevelManager.max_point_z - camera_position_z <= relative_max_obscured_point: break

		if not (0 <= tile_index.x < LevelManager.tile_map_size.x and 0 <= tile_index.y < LevelManager.tile_map_size.y): continue
		tile: dict | None = LevelManager.tile_map[int(tile_index.y)][int(tile_index.x)]
		if tile is None: continue

		tile_height: int = tile["height"]
		relative_tile_bottom: float = tile["position_z"] - camera_position_z
		relative_tile_top: float = relative_tile_bottom - tile_height

		relative_min_tile_point: float = min(relative_tile_top, relative_tile_bottom)
		relative_max_tile_point: float = max(relative_tile_top, relative_tile_bottom)

		min_tile_point_visible: bool = relative_min_tile_point < relative_min_obscured_point
		max_tile_point_visible: bool = relative_max_tile_point > relative_max_obscured_point
		if not (min_tile_point_visible or min_tile_point_visible): continue
		if not tile["transparent"]:
			tan_min_obscured_angle = relative_min_tile_point / distance if min_tile_point_visible else tan_min_obscured_angle
			tan_max_obscured_angle = relative_max_tile_point / distance if max_tile_point_visible else tan_max_obscured_angle

		texture_offset_x: float = abs((ray_position.x % LevelManager.tile_size.x) / LevelManager.tile_size.x - max(ray_sign.y, 0)) % 1
		texture_offset_y: float = abs((ray_position.y % LevelManager.tile_size.y) / LevelManager.tile_size.y + min(ray_sign.x, 0)) % 1
		x_offset_larger_y_offset: bool = texture_offset_x > texture_offset_y

		tile_side_length: int = LevelManager.tile_size.x if x_offset_larger_y_offset else LevelManager.tile_size.y
		texture_offset: float = texture_offset_x if x_offset_larger_y_offset else texture_offset_y

		column_texture = pygame.transform.scale(tile["texture"], (abs(tile_side_length), abs(tile_height))).subsurface(abs(tile_side_length) * texture_offset, 0, 1, abs(tile_height))

		#TODO change texture сut
		#texture: pygame.Surface = tile["texture"]
		#texture_size: tuple[int, int] = texture.get_size()
		#column_width = texture_size[0] / tile_side_length
		#ceil_column_width = math.ceil(column_width)
		#scale_x = texture_size[0] * ceil_column_width / column_width

		#column_texture = pygame.transform.scale(tile["texture"], (scale_x, texture_size[1])).subsurface(min(scale_x * texture_offset,scale_x - ceil_column_width), 0, ceil_column_width, texture_size[1])

		tile_projections.append(calculate_projection(ray_relative_angle_tan, right_ray_relative_angle_tan, distance * ray_relative_angle_cos, relative_tile_top, relative_tile_bottom, column_texture))
	return tile_projections


def line_out_of_bounds(ray_sign: pygame.Vector2, tile_index: pygame.Vector2) -> bool:
	return (
		(ray_sign.x < 0 and tile_index.x < 0) or
		(ray_sign.y < 0 and tile_index.y < 0) or
		(0 < ray_sign.x and LevelManager.tile_map_size.x <= tile_index.x) or
		(0 < ray_sign.y and LevelManager.tile_map_size.y <= tile_index.y))


def calculate_projection(left_ray_relative_angle_tan: float, right_ray_relative_angle_tan: float, distance: float, relative_top: float, relative_bottom: float, texture: pygame.Surface) -> tuple[pygame.Surface, pygame.Vector2, float]:
	projection_position_x: float = left_ray_relative_angle_tan * Settings.resolution_x_div_double_tan_half_fov_h + Settings.half_resolution[0]
	projection_width: float = right_ray_relative_angle_tan * Settings.resolution_x_div_double_tan_half_fov_h + Settings.half_resolution[0] - projection_position_x

	projection_position_y: float = 0
	projection_height: float = 0
	if distance >= 1:
		if relative_bottom < relative_top:
			relative_top, relative_bottom = relative_bottom, relative_top
			texture = pygame.transform.flip(texture, False, True)

		projection_y_factor: float = Settings.resolution_x_div_double_tan_half_fov_h / distance
		projection_position_y = relative_top * projection_y_factor + Settings.half_resolution[1]
		projection_height = relative_bottom * projection_y_factor + Settings.half_resolution[1] - projection_position_y

	projection_position: pygame.Vector2 = pygame.Vector2(math.floor(projection_position_x), math.floor(projection_position_y))
	projection_surface = pygame.transform.scale(texture, (math.ceil(projection_width), math.ceil(projection_height)))

	return (projection_surface, projection_position, distance)
