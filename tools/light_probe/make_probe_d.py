"""Probe D: is the gun inside the light's radius, as the shader sees it? Built from probe A with only the shader swapped.
  red   = 1 - distance / radius to the FIRST light in the list (0 = outside the light)
  green = how much the face turns toward that light (0 = facing away)
  blue  = 1 when the list holds a light at all
"""
import sys
import zipfile

SRC, OUT = sys.argv[1], sys.argv[2]
SHADER_D = """// Light probe D: distance and facing to the first light the held gun receives.
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
            float d = distance(lightpos.xyz, pixelpos.xyz);
            c.r = clamp(1.0 - d / max(lightpos.w, 1.0), 0.0, 1.0);
            c.g = clamp(dot(normalize(vWorldNormal.xyz), normalize(lightpos.xyz - pixelpos.xyz)), 0.0, 1.0);
            c.b = 1.0;
        }
    }
    material.Base = vec4(c, 1.0);
    material.Bright = vec4(1.0);
}
"""
with zipfile.ZipFile(SRC) as zin, zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == "shaders/lightprobe.fp":
            data = SHADER_D.encode()
        zout.writestr(item.filename, data)
print("built", OUT)
