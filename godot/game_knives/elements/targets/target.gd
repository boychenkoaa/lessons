extends CharacterBody2D
class_name Target

const KNIFE_POSITION = Vector2(0, 180)
const APPlE_POSITION = Vector2(0, 190)
const OBJECT_MARGIN := PI / 6
const GENERATION_LIMIT := 10

var knife_scene : PackedScene = load("res://knife.tscn")
var apple_scene : PackedScene = load("res://elements/targets/Scenes/apple.tscn")


var speed := PI

@onready var items_container := $ItemsContainer

func _ready():
	add_default_items(3, 3)

func _physics_process(delta: float):
	rotation += speed * delta
	
func add_obj_with_pivot(object: Node2D, obj_rotation: float):
	var pivot := Node2D.new()
	pivot.rotation = obj_rotation
	pivot.add_child(object)	
	items_container.add_child(pivot)

func get_free_random_rotation(occupied_rotations: Array, generation_attempts: int):
	var is_fail := false
	var random_rotation := 0
	for i in range(generation_attempts):
		random_rotation = Globals.rng.randf_range(0, 2 * PI)
		is_fail = false
		for occupied in occupied_rotations:
			if random_rotation <= occupied + OBJECT_MARGIN / 2.0 and random_rotation >= occupied - OBJECT_MARGIN / 2.0:
				is_fail = true
				break
		if not is_fail:
			return random_rotation
	return null
	
func add_default_items(knives: int, apples: int):
	var occupied_rotations := []
	for i in range(knives):
		var pivot_rotation = get_free_random_rotation(occupied_rotations, GENERATION_LIMIT)
		if pivot_rotation == null:
			return 
			
		occupied_rotations.append(pivot_rotation)
		var knife = knife_scene.instantiate()
		knife.position = KNIFE_POSITION
		add_obj_with_pivot(knife, pivot_rotation)
	
	for i in range(apples):
		var pivot_rotation = get_free_random_rotation(occupied_rotations, GENERATION_LIMIT)
		if pivot_rotation == null:
			return 
			
		occupied_rotations.append(pivot_rotation)
		var apple = apple_scene.instantiate()
		apple.position = APPlE_POSITION
		add_obj_with_pivot(apple, pivot_rotation)
		
