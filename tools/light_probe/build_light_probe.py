"""Build two small probe pk3s that paint, onto the cube shotgun, what the engine's lighting actually receives.

  lightprobe_A.pk3  red   = the surface normal arrived (its length)
                    green = a dynamic-light list was handed to this draw (uLightIndex >= 0)
                    blue  = light that actually reaches the surface after the normal test (sum of lightContribution)
  lightprobe_B.pk3  the normal itself as colour (abs), so each cube face direction gets its own colour

Both also carry a test light actor that hovers above-left of the player (spawned by an event handler, no input
needed), so the gun is always inside a dynamic light's radius during the probe.
"""
import os, sys, zipfile

OUT = sys.argv[1]
SKIN = "models/ashes2063/cubeshotgun/cube_shotgun.png"

COMMON_GLDEFS = """
pointlight LightProbeLight
{
    color 1.0 0.7 0.3
    size 300
}
object LightProbeGlow
{
    frame TNT1 { light LightProbeLight }
}
"""

ZSCRIPT = """version "4.10"

class LightProbeGlow : Actor
{
    Default { +NOGRAVITY +NOBLOCKMAP +NOCLIP }
    States { Spawn: TNT1 A -1; Stop; }
    override void Tick()
    {
        Super.Tick();
        let p = players[consoleplayer].mo;
        if (p) SetOrigin(p.Vec3Angle(50, p.angle, 70), true);   // a little ahead of and above the player, every tic
    }
}

class LightProbeHandler : EventHandler
{
    Actor glow; bool once;
    override void WorldTick()
    {
        if (!once)
        {
            let p = players[consoleplayer].mo;
            if (p) { glow = Actor.Spawn("LightProbeGlow", p.Vec3Angle(50, p.angle, 70)); Console.Printf("LightProbe: glow spawned %s", glow ? "ok" : "FAILED"); once = true; }
        }
    }
}
"""

MAPINFO = """GameInfo
{
    AddEventHandlers = "LightProbeHandler"
}
"""

SHADER_A = """// Light probe A: what the lighting code receives on the held gun.
vec3 lightContribution(int i, vec3 normal);   // defined later in the engine's own light code

void SetupMaterial(inout Material material)
{
    SetMaterialProps(material, vTexCoord.st);
    vec3 n = vWorldNormal.xyz;
    float hasNormal = clamp(length(n), 0.0, 1.0);
    float hasList = (uLightIndex >= 0) ? 1.0 : 0.0;
    vec3 sum = vec3(0.0);
    if (uLightIndex >= 0)
    {
        ivec4 lightRange = ivec4(lights[uLightIndex]) + ivec4(uLightIndex + 1);
        for (int i = lightRange.x; i < lightRange.y; i += 4) sum += lightContribution(i, normalize(n));
    }
    float lit = clamp(max(max(sum.r, sum.g), sum.b), 0.0, 1.0);
    material.Base = vec4(hasNormal, hasList, lit, 1.0);
    material.Bright = vec4(1.0);   // Bright feeds the LIGHT colour, which then multiplies Base: full light, so Base is read as-is
}
"""

SHADER_B = """// Light probe B: the normal itself as colour, one colour per cube face direction.
void SetupMaterial(inout Material material)
{
    SetMaterialProps(material, vTexCoord.st);
    vec3 n = vWorldNormal.xyz;
    vec3 c = (length(n) > 0.001) ? abs(normalize(n)) : vec3(0.0);
    material.Base = vec4(c, 1.0);
    material.Bright = vec4(1.0);
}
"""

def build(name, shader):
    path = os.path.join(OUT, name)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("zscript.lightprobe", ZSCRIPT)
        z.writestr("mapinfo.lightprobe", MAPINFO)
        if shader is None:   # probe C: the light only, the gun keeps its own paint
            z.writestr("gldefs.lightprobe", COMMON_GLDEFS)
        else:
            z.writestr("gldefs.lightprobe", COMMON_GLDEFS + f'\nmaterial texture "{SKIN}"\n{{\n    shader "shaders/lightprobe.fp"\n    speed 0\n}}\n')
            z.writestr("shaders/lightprobe.fp", shader)
    print("built", path)

build("lightprobe_A.pk3", SHADER_A)
build("lightprobe_C.pk3", None)
build("lightprobe_B.pk3", SHADER_B)
