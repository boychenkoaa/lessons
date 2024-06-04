extends Node3D

@onready var  camera = $Camera3D
var torus_material: StandardMaterial3D = StandardMaterial3D.new()
var photo_material: StandardMaterial3D = StandardMaterial3D.new()
var points_shader: Shader = preload("res://plane.gdshader")
var shader_material: ShaderMaterial = ShaderMaterial.new()
@onready var torus_points: MeshInstance3D = $torus_points
@onready var torus: MeshInstance3D = $torus
@onready var light_source = $Light
@onready var selection_rect: Polygon2D = $SelectionRect

var flag: bool = true

var dragging = false  # Are we currently dragging?
var drag_start = Vector2.ZERO  # Location where drag began.
var select_rect = RectangleShape2D.new()  # Collision shape for drag box.


# Called when the node enters the scene tree for the first time.
func _ready():
	shader_material.shader = points_shader
	torus_material.albedo_color = Color(1,0.5,0)
	torus_material.shading_mode = BaseMaterial3D.SHADING_MODE_PER_VERTEX
	torus_material.cull_mode = BaseMaterial3D.CULL_DISABLED
	reset_scene_to_default()
	
	
func take_photo():
	var vpt = get_viewport()
	var txt = vpt.get_texture()
	var image = txt.get_data()
	image.flip_y()
	return image	
	
	
func _input(event):
	var direction = camera.transform.origin.normalized()
	if event is InputEventKey and event.pressed:
		if event.keycode == KEY_W:
			camera.position += camera.get_frustum()[1].normal
		if event.keycode == KEY_S:
			camera.position += -camera.get_frustum()[1].normal
		if event.keycode == KEY_A:
			camera.rotate_y(0.1)	
		if event.keycode == KEY_D:
			camera.rotate_y(-0.1)
		if event.keycode == KEY_SPACE:
			flag = not flag
			if flag:
				prepare_scene_to_photo()
			else:
				reset_scene_to_default()
				
			
	elif event is InputEventMouse:
		if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
			# Start dragging if the click is on the sprite.
			if not dragging and event.pressed:
				dragging = true
				shader_material.set_shader_parameter("dragging", dragging)
				selection_rect.visible = true
		
			# Stop dragging if the button is released.
			if dragging and not event.pressed:
				dragging = false
				shader_material.set_shader_parameter("dragging", dragging)
				selection_rect.visible = false
				
				#selection_rect.visible = false
		if dragging and (event is InputEventMouseMotion):
			selection_rect.position = event.position
			var pos: Vector2 = event.position
			shader_material.set_shader_parameter("xmin", pos[0])
			shader_material.set_shader_parameter("ymin", pos[1])
			var size: Vector2 = selection_rect.polygon[2]
			shader_material.set_shader_parameter("xmax", pos[0]+size[0])
			shader_material.set_shader_parameter("ymax", pos[1]+size[1])
			$Label.text = "SELECTED: " + str( get_selection_by_scrot())
			

		
func prepare_scene_to_photo():
	torus_material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	torus_material.albedo_color = Color(0.0, 0.0, 0.0)
	torus_points.mesh = torus.mesh.duplicate()
	torus_points.set_surface_override_material(0, shader_material)
	torus_points.visible = true
	
func reset_scene_to_default():
	torus_material.shading_mode = BaseMaterial3D.SHADING_MODE_PER_VERTEX
	torus_material.albedo_color = Color(0.0, 1.0, 0.0)
	torus.set_surface_override_material(0,torus_material)
	torus_points.visible = false

func check_color(c: Color):
	return c.b >= 0.99 and c.r <= 0.5

func get_selection_by_scrot():
	var vp_image = get_viewport().get_texture().get_image()
	var count = 0
	for point in torus_points.mesh.get_mesh_arrays()[0]:
		if camera.is_position_in_frustum(point):
			var xy_vp = camera.unproject_position(point)
			var x = int(xy_vp[0])
			var y = int(xy_vp[1])
			var colors =  [vp_image.get_pixel(x, y), vp_image.get_pixel(x-1, y-1), vp_image.get_pixel(x+1, y+1)]
			for c in colors:
				if check_color(c):
					count += 1
					break

	
	return count
				
				
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
