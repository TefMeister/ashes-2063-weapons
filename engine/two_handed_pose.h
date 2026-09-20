// two_handed_pose.h -- how a two-handed long gun is DRAWN (2026-09-20)
//
// Companion to two_handed_aim.h, which decides where the shot GOES. This one decides which way
// the gun POINTS on screen, and it exists because shipping the invisible half first read, from
// inside the headset, as "the left hand does nothing" (owed/HOME, 2026-09-20).
//
// The shape Tefa asked for, in their words: the handle sits in the right hand and the gun
// "shoots to wherever the left controller is". So the rear hand is the ANCHOR -- it keeps the
// gun's position and its twist -- and the off hand only swings the muzzle. How far apart the
// hands are does not matter.
//
// Pure maths, plain doubles, no GZDoom and no OpenVR types, so it can be tested on its own.
// Everything here is in OpenVR's absolute tracking space: right-handed, metres, and the frame's
// FORWARD is -Z (the direction a controller points out of its front).

#pragma once

#include <cmath>

namespace thp
{
	// Below this, the two hands are effectively in the same place and there is no line to aim
	// along. This is a divide-by-zero guard ONLY -- it is deliberately not a "are you really
	// holding it with two hands?" test, because Tefa asked for no such condition.
	constexpr double kMinHandGapMetres = 0.02;	// 2 cm

	// A gun pointed almost exactly along its own up axis leaves no room to work out which way is
	// up any more; below this we rebuild the frame from the old right axis instead.
	constexpr double kDegenerateAxis = 1e-4;

	struct Basis
	{
		// Columns of the rotation: where the frame's local X, Y and Z axes point.
		double x[3];
		double y[3];
		double z[3];
	};

	struct Result
	{
		Basis basis;		// only meaningful when used == true
		double gap;			// how far apart the hands are, in metres
		bool used;			// false -> leave the gun drawn exactly as it is today
	};

	inline void cross3(const double a[3], const double b[3], double out[3])
	{
		out[0] = a[1] * b[2] - a[2] * b[1];
		out[1] = a[2] * b[0] - a[0] * b[2];
		out[2] = a[0] * b[1] - a[1] * b[0];
	}

	inline double length3(const double a[3])
	{
		return std::sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2]);
	}

	inline bool normalize3(double a[3])
	{
		const double len = length3(a);
		if (len < kDegenerateAxis) return false;
		a[0] /= len; a[1] /= len; a[2] /= len;
		return true;
	}

	// rear:  the weapon hand's own frame and position (the anchor).
	// front: the off hand's position. Its rotation is not used -- only where it is.
	inline Result aim_along_hands(const Basis& rear, const double rear_pos[3], const double front_pos[3])
	{
		Result r;
		r.used = false;

		double fwd[3] = { front_pos[0] - rear_pos[0], front_pos[1] - rear_pos[1], front_pos[2] - rear_pos[2] };
		r.gap = length3(fwd);
		if (r.gap < kMinHandGapMetres) return r;

		fwd[0] /= r.gap; fwd[1] /= r.gap; fwd[2] /= r.gap;

		// Forward is -Z, so the new Z axis is the opposite of where we want to point.
		double nz[3] = { -fwd[0], -fwd[1], -fwd[2] };

		// Right-handed frame: X = Y x Z, Y = Z x X. Keeping the rear hand's up axis as the
		// starting point is what preserves the twist of the right wrist.
		double nx[3];
		cross3(rear.y, nz, nx);
		double ny[3];
		if (normalize3(nx))
		{
			cross3(nz, nx, ny);
		}
		else
		{
			// Pointing along the up axis: fall back to the rear hand's right axis.
			cross3(nz, rear.x, ny);
			if (!normalize3(ny)) return r;
			cross3(ny, nz, nx);
		}

		for (int i = 0; i < 3; ++i)
		{
			r.basis.x[i] = nx[i];
			r.basis.y[i] = ny[i];
			r.basis.z[i] = nz[i];
		}
		r.used = true;
		return r;
	}
}
