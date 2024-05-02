extends Node2D
const EXPLOSION_TIME := 2.0

var is_hited := false
@onready var apple_particles_list = [$AppleParticles2D1, $AppleParticles2D2]
@onready var sprite = $Sprite2D

func _explode_animation():
	var tween := create_tween()
	
	for apple_particles in apple_particles_list:
		apple_particles.emitting = true
		tween.parallel().tween_property(apple_particles, "modulate", Color("ffffff00"), EXPLOSION_TIME)
	
	tween.play()
	await tween.finished

func _ready():
	pass

func _on_area_2d_body_entered(body):
	if not is_hited:
		is_hited = true
		sprite.hide()
		var tween := create_tween()
	
		for apple_particles in apple_particles_list:
			apple_particles.emitting = true
			tween.parallel().tween_property(apple_particles, "modulate", Color("ffffff00"), EXPLOSION_TIME)
		
		tween.play()
		await tween.finished
		queue_free()
		
