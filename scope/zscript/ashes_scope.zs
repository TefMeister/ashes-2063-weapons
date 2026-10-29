// Ashes 2063: a live scope on the FAL's box sight (ashes-2063-weapons/scope, 2026-10-29).
//
// The FAL's eyepiece glass is its own model surface, always surface 0 (brutal-doom-3d-guns/tools/gz_forge_export.py,
// forge part "glass"). While the FAL is the ready weapon, a hidden camera rides the gun hand, looking where the gun
// points, and its picture is drawn on that glass at MAG times zoom. Any other weapon: the glass gets its plain skin back
// and the camera is removed, so nothing extra is rendered.
//
// The method (a camera texture, and the glass surface's skin swapped with A_ChangeModel / CMDL_USESURFACESKIN) is the
// one the scope in the BD22Q VR pack uses, which another Brutal Doom VR modder kindly sent Tefa on 2026-10-29. This file
// is our own code for our engine's gun-hand fields (AttackPos, AttackAngle, AttackPitch, AttackRoll); none of the pack's
// code is copied into it.
//
// Not yet run in the game [hypothesis]: the pitch and roll signs, the picture's left-right, and whether a tic-rate
// camera reads as jittery in the headset all wait for the first look.

class AshesScopeCam : Actor
{
	Default
	{
		+NOBLOCKMAP
		+NOGRAVITY
		+DONTSPLASH
		+NOTONAUTOMAP
		RenderStyle "None";
	}
}

class AshesScope : EventHandler
{
	const TEXNAME = "ASHSCOPE";		// ANIMDEFS: eight characters, or the engine never finds it again
	const GLASS = 0;				// the glass surface (gz_forge_export.py puts it first)
	const MAG = 3.0;				// zoom
	const LENS_FOV = 30.0;			// degrees the glass covers at the eye [hypothesis]; the view shows 1/MAG of it

	AshesScopeCam cam;
	Weapon skinned;

	static bool Scoped(Weapon w)
	{
		return w && w.GetClassName() == 'FAL';
	}

	override void WorldLoaded(WorldEvent e)
	{
		cam = null;				// the old level's actors are gone
		skinned = null;
	}

	override void WorldTick()
	{
		let p = players[consoleplayer];
		let mo = p.mo;
		Weapon w = mo ? p.ReadyWeapon : null;
		if (!Scoped(w))
		{
			Off();
			return;
		}
		if (skinned != w)
		{
			Off();
			w.A_ChangeModel('None', 0, "", 'None', GLASS, "", TEXNAME, CMDL_USESURFACESKIN);
			skinned = w;
		}
		Vector3 at;
		double ang, pit, rol;
		if (mo.OverrideAttackPosDir)		// VR: where the gun hand is and points
		{
			at = mo.AttackPos;
			ang = mo.AttackAngle;
			pit = mo.AttackPitch;
			rol = mo.AttackRoll;
		}
		else							// flat: the player's own eye
		{
			at = (mo.pos.xy, p.viewz);
			ang = mo.angle;
			pit = mo.pitch;
			rol = mo.roll;
		}
		if (!cam)
		{
			cam = AshesScopeCam(Actor.Spawn('AshesScopeCam', at));
			TexMan.SetCameraToTexture(cam, TEXNAME, LENS_FOV / MAG);
		}
		cam.SetOrigin(at, true);
		cam.A_SetAngle(ang, SPF_INTERPOLATE);
		cam.A_SetPitch(pit, SPF_INTERPOLATE);
		cam.A_SetRoll(rol, SPF_INTERPOLATE);
	}

	void Off()
	{
		if (skinned)		// 'None' falls back to the MODELDEF SurfaceSkin: the plain glass
			skinned.A_ChangeModel('None', 0, "", 'None', GLASS, "", 'None', CMDL_USESURFACESKIN);
		skinned = null;
		if (cam)
			cam.Destroy();
		cam = null;
	}
}
