shader_type spatial;
render_mode unshaded;

uniform float xmin = 0.0;
uniform float xmax = 0.0;
uniform float ymin = 0.0;
uniform float ymax = 0.0;
uniform bool dragging = false;
uniform bool is_red = true;

//render_mode shadows_disabled;

void vertex() {
	//vert_id = float(VERTEX_ID);
	POINT_SIZE = 5.0;
}

void fragment() {
	if (dragging)
	{
		if ((FRAGCOORD.x <= xmax) && (FRAGCOORD.x >= xmin) &&  (FRAGCOORD.y <= ymax) && (FRAGCOORD.y >= ymin)  && FRONT_FACING )
		{
			ALBEDO = vec3(0.0, 0.0, 1.0);
		}
	}
}

//void light() {
	// Called for every pixel for every light affecting the material.
	// Uncomment to replace the default light processing function with this one.
//}
