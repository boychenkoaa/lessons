extends CharacterBody2D

enum State {IDLE, FLY_TO_TARGET, FLY_AWAY}

var state := State.IDLE
var speed := 4500
var fly_away_speed := 1000.0
var fly_away_rotation_speed := 4500.0
var fly_away_direction = Vector2.DOWN
var fly_away_deviation := PI/4

func change_state(new_state: State):
	state = new_state

func throw():
	change_state(State.FLY_TO_TARGET)
	
func throw_away(direction: Vector2):
	var random_deviation = Globals.rng.randf_range(-fly_away_deviation, fly_away_deviation)
	fly_away_direction = direction.rotated(random_deviation)
	change_state(State.FLY_AWAY)

func _physics_process(delta: float):
	if state == State.FLY_TO_TARGET:
		var collision = move_and_collide(Vector2.UP * delta * speed)
		if collision:
			handle_collision(collision)
		
	elif state == State.FLY_AWAY:
		global_position += fly_away_direction * fly_away_speed * delta
		rotation += fly_away_rotation_speed * delta

func handle_collision(collision: KinematicCollision2D):
	var collider = collision.get_collider()
	if collider is Target:
		add_knife_to_target(collider)
		change_state(State.IDLE)
	else:
		throw_away(collision.get_normal())
		
		
func add_knife_to_target(target: Target):
	get_parent().remove_child(self)
	global_position = Target.KNIFE_POSITION
	rotation = 0
	target.add_object_to_pivot(self, -target.rotation)
	

"""
const SPEED = 300.0
const JUMP_VELOCITY = -400.0

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")


func _physics_process(delta):
	# Add the gravity.
	if not is_on_floor():
		velocity.y += gravity * delta

	# Handle jump.
	if Input.is_action_just_pressed("ui_accept") and is_on_floor():
		velocity.y = JUMP_VELOCITY

	# Get the input direction and handle the movement/deceleration.
	# As good practice, you should replace UI actions with custom gameplay actions.
	var direction = Input.get_axis("ui_left", "ui_right")
	if direction:
		velocity.x = direction * SPEED
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED)

	move_and_slide()
"""
