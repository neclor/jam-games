extends Node2D


var map_size: Vector2i = Vector2i(64, 64)


@onready var map_tile_map_layer: TileMapLayer = $MapTileMapLayer
@onready var waves_tile_map_layer: TileMapLayer = $WavesTileMapLayer


func _ready() -> void:
	Global.time = 0
	draw_map()
	draw_waves()

func _physics_process(delta: float) -> void:
	Global.time += delta
	Global.seconds = fmod(Global.time, 60)
	Global.minutes = fmod(Global.time, 3600) / 60


func draw_map() -> void:
	var map_cells: Array[Vector2i] = []
	for x in range(-map_size.x / 2 - 1, map_size.x / 2 + 1):
		for y in range(-map_size.y / 2 - 1, map_size.y / 2 + 1):
			map_cells.append(Vector2i(x, y))
	map_tile_map_layer.set_cells_terrain_connect(map_cells, 0, 0)


func draw_waves() -> void:
	var waves_cells: Array[Vector2i] = []
	for x in range(-map_size.x / 2, map_size.x / 2):
		for y in range(-map_size.y / 2, map_size.y / 2):
			waves_cells.append(Vector2i(x, y))
	waves_tile_map_layer.set_cells_terrain_connect(waves_cells, 0, 0)
