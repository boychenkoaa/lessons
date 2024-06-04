extends Node3D

@onready var  camera = $Camera3D
@onready var torus_points: MeshInstance3D = $torus_points
@onready var torus: MeshInstance3D = $torus
@onready var light_source = $Light
@onready var selection_rect: Line2D = $SelectionRect

var torus_material: StandardMaterial3D = StandardMaterial3D.new()
var photo_material: StandardMaterial3D = StandardMaterial3D.new()
var points_shader: Shader = preload("res://plane.gdshader")
var shader_material: ShaderMaterial = ShaderMaterial.new()
var is_dragging = false  
const COLOR_EPSILON: float = 0.01
const SELECTION_COLOR: Color = Color(1,0,1)
var select_rect = RectangleShape2D.new()  # Collision shape for drag box.

func prepare_materials():
	torus_material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	torus_material.albedo_color = Color(0.0, 0.0, 0.0)
	torus_material.cull_mode = BaseMaterial3D.CULL_DISABLED
	torus.set_surface_override_material(0, torus_material)
	shader_material.shader = points_shader
	torus_points.mesh = torus.mesh.duplicate()
	torus_points.set_surface_override_material(0, shader_material)
	
func drag_proccess(pos: Vector2i):
	selection_rect.position = pos
	shader_material.set_shader_parameter("xmin", pos[0])
	shader_material.set_shader_parameter("ymin", pos[1])
	var size: Vector2 = selection_rect.points[2]
	shader_material.set_shader_parameter("xmax", pos[0]+size[0])
	shader_material.set_shader_parameter("ymax", pos[1]+size[1])
	torus.visible = false
	$Label.text = "SELECTED: " + str(get_selection_count())
	torus.visible = true
	
func dragging_start():
	is_dragging = true
	shader_material.set_shader_parameter("dragging", is_dragging)
	selection_rect.visible = true
	
func dragging_finish():
	is_dragging = false
	shader_material.set_shader_parameter("dragging", is_dragging)
	selection_rect.visible = false

func _ready():
	prepare_materials()
	
func _input(event):
	var direction = camera.transform.origin.normalized()
	
	if event is InputEventKey:
		if event.keycode == KEY_A:
			camera.rotate_y(0.1)
		if event.keycode == KEY_D:
			camera.rotate_y(-0.1)
		if event.keycode == KEY_W:
			camera.rotate_z(0.1)
		if event.keycode == KEY_S:
			camera.rotate_z(-0.1)
		if event.keycode == KEY_Q:
			camera.rotate_x(-0.1)	
		if event.keycode == KEY_E:
			camera.rotate_x(0.1)	
		
	if event is InputEventMouse:
		if event is InputEventMouseButton:
			if event.button_index == MOUSE_BUTTON_WHEEL_UP :
				camera.position += camera.get_frustum()[1].normal
			if event.button_index == MOUSE_BUTTON_WHEEL_DOWN :
				camera.position -= camera.get_frustum()[1].normal
			if event.button_index == MOUSE_BUTTON_LEFT:
				if not is_dragging and event.pressed:
					dragging_start()
				if is_dragging and not event.pressed:
					dragging_finish()
					
		if event is InputEventMouseMotion:	
			if is_dragging:
				drag_proccess(event.position)
		
func validate_color(color: Color, target_color: Color = SELECTION_COLOR, epsilon: float = COLOR_EPSILON):
	return Vector3(color[0], color[1], color[2]).distance_to(Vector3(target_color[0], target_color[1], target_color[2])) <= epsilon

func get_selection_count():
	var vp_image = get_viewport().get_texture().get_image()
	var count = 0
	for point in torus_points.mesh.get_mesh_arrays()[0]:
		if not camera.is_position_behind(point) and camera.is_position_in_frustum(point):
			var xy_vp = camera.unproject_position(point)
			var x = xy_vp[0]
			var y = xy_vp[1]
			if x < vp_image.get_width()-1 and x>0 and y < vp_image.get_height()-1 and y>0:
				var colors =  [vp_image.get_pixel(x, y), vp_image.get_pixel(x-1, y-1), vp_image.get_pixel(x+1, y+1)]
				for color in colors:
					if validate_color(color):
						count += 1
						break
	return count

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
