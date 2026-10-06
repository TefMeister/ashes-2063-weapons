// cube_shine.fp -- a shine on the cube weapons that needs no light from the game (Tefa, 2026-10-06:
// "light reflections to our gun model that don't need light source from the game and just has a shine to it as it
// turns in VR").
//
// How: GZDoom hands a material shader the surface's world position (pixelpos), its world normal (vWorldNormal) and
// the eye position (uCameraPos). From those, the mirror direction of the view is known, and a soft made-up "window"
// of light fixed in the world is tested against it. The result goes into Material.Bright, which GZDoom ADDS after
// the room's own lighting (main.fp: color.rgb = min(color.rgb + material.Bright.rgb, 1.0)), so it shows in the
// darkest corridor. Turn the gun or your head and each flat cube face catches the glint at its own angle.
//
// Only grey metal shines fully (low colour saturation); wood and cloth barely; lighter texels (scratches, worn
// edges) glint more. Every number is in the block below.

const vec3  SHINE_DIR      = vec3(0.35, 0.85, 0.40); // where the made-up light window sits (GL world: y is up)
const float SHINE_SHARP    = 18.0;   // higher = smaller, sharper glint
const float SHINE_STRENGTH = 0.30;   // how bright the glint gets at its peak
const float RIM_STRENGTH   = 0.06;   // a faint sheen on faces seen edge-on
const float SCRATCH_BOOST  = 2.2;    // light texels (scratches, worn edges) glint this much more
const float METAL_SAT      = 0.12;   // above this colour saturation a texel counts as not metal

void SetupMaterial(inout Material material)
{
	vec2 texCoord = GetTexCoord();
	SetMaterialProps(material, texCoord);

	vec3 base = material.Base.rgb;
	float hi = max(max(base.r, base.g), base.b);
	float lo = min(min(base.r, base.g), base.b);
	float sat = hi > 0.001 ? (hi - lo) / hi : 0.0;
	float metal = clamp(1.0 - sat / METAL_SAT, 0.0, 1.0);
	float scratch = 1.0 + SCRATCH_BOOST * smoothstep(0.20, 0.45, hi);

	vec3 n = normalize(vWorldNormal.xyz);
	vec3 v = normalize(uCameraPos.xyz - pixelpos.xyz);
	vec3 r = reflect(-v, n);
	float glint = pow(max(dot(r, normalize(SHINE_DIR)), 0.0), SHINE_SHARP);
	float rim = pow(1.0 - max(dot(n, v), 0.0), 4.0);

	float s = metal * (glint * SHINE_STRENGTH * scratch + rim * RIM_STRENGTH);
	material.Bright = vec4(material.Bright.rgb + vec3(s), material.Bright.a);
}
