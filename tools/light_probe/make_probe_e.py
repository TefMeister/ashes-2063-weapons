"""Probes E1/E2: which factor of the engine's lightContribution() is zero on the held gun in VR.
Built from probe A with only the shader swapped. Both take the FIRST light anywhere in the gun's list.
  E1  red   = 1 when that light sits in the normal (modulated) section, 0 when in subtractive/additive
      green = shadowAttenuation() for it (1 = not shadowed)
      blue  = 1 when it is flagged as a spot light
  E2  the light's own colour as the shader receives it (orange 1.0/0.7/0.3 expected), black = no light at all
    python make_probe_e.py <probe A pk3> <out E1 pk3> <out E2 pk3>
"""
import sys
import zipfile

SRC, OUT1, OUT2 = sys.argv[1], sys.argv[2], sys.argv[3]
HEAD = """float shadowAttenuation(vec4 lightpos, float lightcolorA);   // defined later in the engine's own light code

void SetupMaterial(inout Material material)
{
    SetMaterialProps(material, vTexCoord.st);
    vec3 c = vec3(0.0);
    if (uLightIndex >= 0)
    {
        ivec4 lightRange = ivec4(lights[uLightIndex]) + ivec4(uLightIndex + 1);
        int i = lightRange.x;
        if (i < lightRange.w)
        {
            vec4 lightpos = lights[i];
            vec4 lightcolor = lights[i + 1];
            vec4 lightspot1 = lights[i + 2];
"""
TAIL = """        }
    }
    material.Base = vec4(c, 1.0);
    material.Bright = vec4(1.0);
}
"""
E1 = ("// Light probe E1: section, shadow, spot flag of the first light on the held gun.\n" + HEAD +
      "            c.r = (i < lightRange.y) ? 1.0 : 0.0;\n"
      "            c.g = clamp(shadowAttenuation(lightpos, lightcolor.a), 0.0, 1.0);\n"
      "            c.b = (lightspot1.w == 1.0) ? 1.0 : 0.0;\n" + TAIL)
E2 = ("// Light probe E2: the first light's colour as the held gun's shader receives it.\n" + HEAD +
      "            c = clamp(lightcolor.rgb, 0.0, 1.0);\n" + TAIL)

for out, shader in ((OUT1, E1), (OUT2, E2)):
    with zipfile.ZipFile(SRC) as zin, zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "shaders/lightprobe.fp":
                data = shader.encode()
            zout.writestr(item.filename, data)
    print("built", out)
