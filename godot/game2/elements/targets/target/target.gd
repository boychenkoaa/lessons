extends CharacterBody2D
class_name Target

const KNIFE_POSITION = Vector2(0, 180)
const APPLE_POSITION = Vector2(0, 176)
const OBJECT_MARGIN := PI/6
const EXPLOSION_TIME := 1

const DEFAULT_KNIVES_COUNT = 2
const DEFAULT_APPLES_COUNT = 1

var knife_scene: PackedScene = load("res://elements/knife/knife.tscn")
var apple_scene: PackedScene = load("res://elements/apple/apple.tscn")

@onready var items_container := $ItemsContainer
@onready var sprite := $Sprite2D
@onready var knife_particles := $KnifeParticles2D
@onready var target_particles_list = [$TargetParticles2D1, $TargetParticles2D2, $TargetParticles2D3]

var speed := PI

func _ready():
	add_default_items(2, 3)
	
	
func _explode():
	sprite.hide()
	items_container.hide()
	
	var tween := create_tween()
	
	for target_particles in target_particles_list:
		tween.parallel().tween_property(target_particles, "modulate", Color("ffffff00"), EXPLOSION_TIME)
		target_particles.emitting = true
	
	knife_particles.rotation = -rotation
	knife_particles.emitting = true
	
	tween.parallel().tween_property(knife_particles, "modulate", Color("ffffff00"), EXPLOSION_TIME)

func _physics_process(delta: float):
	rotation += speed * delta

func add_object_to_pivot(object: Node2D, object_rotation: float):
	var pivot := Node2D.new()
	pivot.rotation = object_rotation
	pivot.add_child(object)
	items_container.add_child(pivot)

func add_default_items(knives_count: int = DEFAULT_KNIVES_COUNT, apples_count: int=DEFAULT_APPLES_COUNT):
	var occupied_rotations = []
	for knife_index in range(knives_count):
		var new_rotation = get_free_random_rotation(occupied_rotations)
		occupied_rotations.append(new_rotation)
		var knife = knife_scene.instantiate()
		knife.position  = KNIFE_POSITION
		add_object_to_pivot(knife, new_rotation)
	
	for apple_index in range(apples_count):
		var new_rotation = get_free_random_rotation(occupied_rotations)
		occupied_rotations.append(new_rotation)
		var apple = apple_scene.instantiate()
		apple.position  = APPLE_POSITION
		add_object_to_pivot(apple, new_rotation)
		

func get_free_random_rotation(occupied_rotations: Array):
	var random_rotation = 0
	var is_free := false
	while not is_free:
		random_rotation = Globals.rng.randf_range(0, 2 * PI)
		is_free = true
		for occupied in occupied_rotations:
			if (abs(random_rotation-occupied) <= OBJECT_MARGIN):
				is_free = false
				break
	return random_rotation
	
