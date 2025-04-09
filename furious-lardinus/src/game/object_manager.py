import pygame


import game.object_class_manager as ClassManager
import game.level_manager as LevelManager


game_objects: list[dict] = []
add_queue: list[dict] = []
remove_queue: list[dict] = []


def update(delta: float) -> None:
	update_game_objects(delta)
	handle_collisions()
	remove_objects()
	add_objects()


def add_object(game_object: dict) -> None:
	add_queue.append(game_object)


def add_objects() -> None:
	global game_objects, add_queue
	game_objects += add_queue
	add_queue = []


def remove_object(game_object: dict) -> None:
	game_object["freed"] = True
	remove_queue.append(game_object)


def remove_objects() -> None:
	global remove_queue
	for game_object in remove_queue:
		if game_object in game_objects: game_objects.remove(game_object)
	remove_queue = []


def update_game_objects(delta: float) -> None:
	for game_object in game_objects:
		if game_object["freed"]: continue
		ClassManager.update(game_object, delta)


def handle_collisions() -> None:
	for i, game_object in enumerate(game_objects):
		if game_object["freed"]: continue
		handle_objects_collisions(game_object, i)
		handle_tile_map_collision(game_object)


def handle_objects_collisions(game_object: dict, index: int) -> None:
	for game_object_2 in game_objects[index + 1:]:
		handle_object_collision(game_object, game_object_2)


def handle_object_collision(game_object: dict, game_object_2: dict) -> None:
	detect_collision, detect_collision_2 = check_collision_layers(game_object, game_object_2)
	if not (detect_collision or detect_collision_2): return

	position: pygame.Vector2 = game_object["position"]
	position_2: pygame.Vector2 = game_object_2["position"]
	radius: int = game_object["radius"]
	radius_2: int = game_object_2["radius"]

	vector_to_object: pygame.Vector2 = position - position_2
	distance: float = vector_to_object.length()
	overlap: float = radius + radius_2 - distance
	handle_collision(game_object, detect_collision, game_object_2, detect_collision_2, vector_to_object, distance, overlap)


def handle_tile_map_collision(game_object: dict) -> None:
	position: pygame.Vector2 = game_object["position"]
	radius: int = game_object["radius"]

	min_tile_index_x: int = int(max(0, (position.x - radius) // LevelManager.tile_size.x))
	max_tile_index_x: int = int(min((position.x + radius) // LevelManager.tile_size.x, LevelManager.tile_map_size.x - 1))
	min_tile_index_y: int = int(max(0, (position.y - radius) // LevelManager.tile_size.y))
	max_tile_index_y: int = int(min((position.y + radius) // LevelManager.tile_size.y, LevelManager.tile_map_size.y - 1))

	for tile_index_y in range(min_tile_index_y, max_tile_index_y + 1):
		for tile_index_x in range(min_tile_index_x, max_tile_index_x + 1):
			tile: dict | None = LevelManager.tile_map[tile_index_y][tile_index_x]
			if tile is None: continue

			detect_collision, _ = check_collision_layers(game_object, tile)
			if not detect_collision: continue

			nearest_tile_point: pygame.Vector2 = find_nearest_tile_point(position, tile_index_x, tile_index_y)
			vector_to_tile: pygame.Vector2 = position - nearest_tile_point
			distance: float = vector_to_tile.length()
			overlap: float = radius - distance
			handle_collision(game_object, True, tile, False, vector_to_tile, distance, overlap)


def find_nearest_tile_point(position: pygame.Vector2, tile_index_x: int, tile_index_y: int) -> pygame.Vector2:
	tile_position: pygame.Vector2 = pygame.Vector2(tile_index_x * LevelManager.tile_size.x, tile_index_y * LevelManager.tile_size.y)
	nearest_tile_point_x: float = pygame.math.clamp(position.x, tile_position.x, tile_position.x + LevelManager.tile_size.x)
	nearest_tile_point_y: float = pygame.math.clamp(position.y, tile_position.y, tile_position.y + LevelManager.tile_size.y)
	return pygame.Vector2(nearest_tile_point_x, nearest_tile_point_y)


def handle_collision(game_object: dict, detect_collision: bool, game_object_2: dict, detect_collision_2: bool, vector_to_object: pygame.Vector2, distance: float, overlap: float) -> None:
	if overlap <= 0: return

	if detect_collision: ClassManager.object_collided(game_object, game_object_2)
	if detect_collision_2: ClassManager.object_collided(game_object_2, game_object)


	if game_object["class"] == "WizzardProjectile" or game_object_2["class"] == "WizzardProjectile": pass

	if not (game_object["collidable"] and game_object_2["collidable"]): return

	static: bool = game_object["static"]
	static_2: bool = game_object_2["static"]
	if static and static_2: return

	if distance == 0: return
	collision_vector: pygame.Vector2 = vector_to_object.normalize() * overlap
	if static_2: game_object["position"] += collision_vector
	elif static: game_object_2["position"] -= collision_vector
	else:
		game_object["position"] += collision_vector / 2
		game_object_2["position"] -= collision_vector / 2


def check_collision_layers(game_object_1: dict, game_object_2: dict) -> tuple[bool, bool]:
	collision_layer_1: int = game_object_1["collision_layer"]
	collision_layer_2: int = game_object_2["collision_layer"]
	collision_mask_1: int | None = game_object_1.get("collision_mask")
	collision_mask_2: int | None = game_object_2.get("collision_mask")
	detect_collision_1: bool = False
	detect_collision_2: bool = False
	if collision_mask_1 is not None:
		detect_collision_1 = (collision_mask_1 & collision_layer_2) > 0
	if collision_mask_2 is not None:
		detect_collision_2 = (collision_mask_2 & collision_layer_1) > 0
	return (detect_collision_1, detect_collision_2)
