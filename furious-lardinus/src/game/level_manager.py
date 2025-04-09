import pygame


import game.game as Game
import game.levels as Levels
import game.object_manager as ObjectManager


import game.objects.active_objects.ammo as Ammo
import game.objects.active_objects.medikit as Medikit
import game.objects.active_objects.exit as Exit


import game.objects.dynamic_objects.entities.enemies.knight as Knight
import game.objects.dynamic_objects.entities.enemies.skull as Skull
import game.objects.dynamic_objects.entities.enemies.summoner as Summoner
import game.objects.dynamic_objects.entities.enemies.wizzard as Wizzard
import game.objects.dynamic_objects.entities.enemies.boss as Boss

floor_color: pygame.Color

tile_size: pygame.Vector2
tile_map_size: pygame.Vector2
tile_map: list[list[dict | None]]

min_point_z: float
max_point_z: float


levels_list: list[str] = [Levels.TUTORIAL_ROOM, Levels.MIDDLE, Levels.B_37, Levels.END_ROOM]
current_level: int = 0


def next_level() -> None:
	global current_level
	if current_level < len(levels_list) + 1: current_level += 1
	load_level()


def load_level() -> None:
	global floor_color, tile_size, tile_map_size, tile_map, min_point_z, max_point_z

	level_data: dict = parse_level_string(levels_list[current_level], Levels.TILE_SET, Levels.OBJECT_SET)
	floor_color = level_data["floor_color"]
	tile_size = level_data["tile_size"]
	tile_map_size = level_data["tile_map_size"]
	tile_map = level_data["tile_map"]
	min_point_z = level_data["min_point_z"]
	max_point_z = level_data["max_point_z"]

	Game.player["position"] = level_data["spawn_point"]

	ObjectManager.game_objects = [Game.player] + level_data["level_objects"]
	ObjectManager.add_queue = []
	ObjectManager.remove_queue = []


def parse_level_string(string: str, tile_set: dict, object_set: dict) -> dict:
	tile_size: pygame.Vector2 = tile_set["tile_size"]
	tiles: dict = tile_set["tiles"]
	objects: dict = object_set["objects"]

	string = string.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
	string = string.rstrip("/")
	rows: list[str] = string.split("/")

	name: str = rows[0]
	floor_color: pygame.Color = pygame.Color(rows[1])
	tile_map_size: pygame.Vector2 = pygame.Vector2(len(rows[2]), len(rows) - 2)

	spawn_point: pygame.Vector2 = pygame.Vector2()
	min_point_z: float = 0
	max_point_z: float = 0
	tile_map: list[list[dict | None]] = []
	level_objects: list[dict] = []
	for y, row in enumerate(rows[2:]):
		tile_row: list[dict | None] = []
		for x, char in enumerate(row):
			tile_center_position: pygame.Vector2 = pygame.Vector2(x * tile_size.x + tile_size.x // 2, y * tile_size.y + tile_size.y // 2)
			if char == "S": spawn_point = tile_center_position

			tile: dict | None = tiles.get(char)
			tile_row.append(tile)
			if tile is not None:
				tile_bottom: float = tile["position_z"]
				tile_top: float = tile_bottom - tile["height"]
				min_point_z = min(tile_top, tile_bottom, min_point_z)
				max_point_z = max(tile_top, tile_bottom, max_point_z)

			level_object: dict | None = new_level_object(objects.get(char), tile_center_position)
			if level_object is not None: level_objects.append(level_object)
		tile_map.append(tile_row)
	return {
		"floor_color": floor_color,
		"tile_size": tile_size,
		"tile_map_size": tile_map_size,
		"tile_map": tile_map,
		"min_point_z": min_point_z,
		"max_point_z": max_point_z,
		"spawn_point": spawn_point,
		"level_objects": level_objects,
	}


def new_level_object(class_name: str | None, position: pygame.Vector2) -> dict | None:
	match class_name:
		case "Ammo": return Ammo.new(position)
		case "Medikit": return Medikit.new(position)
		case "Knight": return Knight.new(position)
		case "Skull": return Skull.new(position)
		case "Summoner": return Summoner.new(position)
		case "Wizzard": return Wizzard.new(position)
		case "Exit": return Exit.new(position)
		case "Boss": return Boss.new(position)
	return None
