// stepped_glide.h -- the "framey but not teleporting" weapon hand (2026-11-11)
//
// Tefa: "make ashes guns move like framey but not teleport, so that the guns still moves smoothly
// but the position of it changes maybe 10FPS".
//
// The stop-motion hand of 2026-09-17 FROZE the gun between updates and then jumped it to the new
// place; that read as teleporting and was dropped. This is the same rhythm without the jump: a few
// times a second (kDefaultStepsPerSecond) the gun is given a new place to be -- where the hand is
// right now -- and it GLIDES there, easing out of the old place and into the new one, on every
// rendered frame. With the glide at 100 % of the step the gun never stops, it only pulses; lower,
// it arrives early and rests until the next step (more of a stop-motion look, still no jump).
//
// Pure maths, plain doubles, no GZDoom and no OpenVR types, so it can be tested on its own
// (stepped_glide_test.cpp). A pose is a 3x4 matrix, rows = x y z, column 3 = position, the layout
// of OpenVR's HmdMatrix34_t.

#pragma once

#include <cmath>

namespace sgl
{
	constexpr int kDefaultStepsPerSecond = 10;	// Tefa's "maybe 10FPS"
	constexpr int kMinStepsPerSecond = 2;
	constexpr int kMaxStepsPerSecond = 30;
	constexpr int kDefaultGlidePercent = 100;	// share of each step spent moving
	constexpr int kMinGlidePercent = 10;
	// A step longer than this means the game was paused, loading or hitching: start again from the
	// live pose rather than glide across the room.
	constexpr double kStaleSeconds = 0.75;

	struct Quat { double w, x, y, z; };

	struct Pose
	{
		double pos[3];
		Quat rot;
	};

	inline Quat Normalize(Quat q)
	{
		const double n = std::sqrt(q.w * q.w + q.x * q.x + q.y * q.y + q.z * q.z);
		if (n < 1e-12) return { 1, 0, 0, 0 };
		return { q.w / n, q.x / n, q.y / n, q.z / n };
	}

	// Rotation part of a 3x4 pose -> quaternion (Shepperd's method, stable for every rotation).
	template <class M34>
	inline Pose FromMatrix(const M34& m)
	{
		Pose p;
		p.pos[0] = m[0][3]; p.pos[1] = m[1][3]; p.pos[2] = m[2][3];
		const double m00 = m[0][0], m11 = m[1][1], m22 = m[2][2];
		const double tr = m00 + m11 + m22;
		Quat q;
		if (tr > 0)
		{
			const double s = std::sqrt(tr + 1.0) * 2;
			q = { 0.25 * s, (m[2][1] - m[1][2]) / s, (m[0][2] - m[2][0]) / s, (m[1][0] - m[0][1]) / s };
		}
		else if (m00 > m11 && m00 > m22)
		{
			const double s = std::sqrt(1.0 + m00 - m11 - m22) * 2;
			q = { (m[2][1] - m[1][2]) / s, 0.25 * s, (m[0][1] + m[1][0]) / s, (m[0][2] + m[2][0]) / s };
		}
		else if (m11 > m22)
		{
			const double s = std::sqrt(1.0 + m11 - m00 - m22) * 2;
			q = { (m[0][2] - m[2][0]) / s, (m[0][1] + m[1][0]) / s, 0.25 * s, (m[1][2] + m[2][1]) / s };
		}
		else
		{
			const double s = std::sqrt(1.0 + m22 - m00 - m11) * 2;
			q = { (m[1][0] - m[0][1]) / s, (m[0][2] + m[2][0]) / s, (m[1][2] + m[2][1]) / s, 0.25 * s };
		}
		p.rot = Normalize(q);
		return p;
	}

	template <class M34>
	inline void ToMatrix(const Pose& p, M34& m)
	{
		const Quat q = p.rot;
		const double xx = q.x * q.x, yy = q.y * q.y, zz = q.z * q.z;
		const double xy = q.x * q.y, xz = q.x * q.z, yz = q.y * q.z;
		const double wx = q.w * q.x, wy = q.w * q.y, wz = q.w * q.z;
		m[0][0] = (decltype(m[0][0] + 0))(1 - 2 * (yy + zz)); m[0][1] = (decltype(m[0][0] + 0))(2 * (xy - wz)); m[0][2] = (decltype(m[0][0] + 0))(2 * (xz + wy));
		m[1][0] = (decltype(m[0][0] + 0))(2 * (xy + wz)); m[1][1] = (decltype(m[0][0] + 0))(1 - 2 * (xx + zz)); m[1][2] = (decltype(m[0][0] + 0))(2 * (yz - wx));
		m[2][0] = (decltype(m[0][0] + 0))(2 * (xz - wy)); m[2][1] = (decltype(m[0][0] + 0))(2 * (yz + wx)); m[2][2] = (decltype(m[0][0] + 0))(1 - 2 * (xx + yy));
		m[0][3] = (decltype(m[0][0] + 0))p.pos[0]; m[1][3] = (decltype(m[0][0] + 0))p.pos[1]; m[2][3] = (decltype(m[0][0] + 0))p.pos[2];
	}

	// Straight line for the position, shortest arc for the rotation.
	inline Pose Blend(const Pose& a, const Pose& b, double s)
	{
		Pose r;
		for (int i = 0; i < 3; ++i) r.pos[i] = a.pos[i] + (b.pos[i] - a.pos[i]) * s;
		Quat q = b.rot;
		double d = a.rot.w * q.w + a.rot.x * q.x + a.rot.y * q.y + a.rot.z * q.z;
		if (d < 0) { q = { -q.w, -q.x, -q.y, -q.z }; d = -d; }
		double ka, kb;
		if (d > 0.9995) { ka = 1 - s; kb = s; }	// nearly the same: a straight blend is exact enough
		else
		{
			const double th = std::acos(d), sn = std::sin(th);
			ka = std::sin((1 - s) * th) / sn;
			kb = std::sin(s * th) / sn;
		}
		r.rot = Normalize({ a.rot.w * ka + q.w * kb, a.rot.x * ka + q.x * kb, a.rot.y * ka + q.y * kb, a.rot.z * ka + q.z * kb });
		return r;
	}

	// Ease out of the old place and into the new one: no speed at either end, so no visible snap.
	inline double Ease(double t)
	{
		if (t <= 0) return 0;
		if (t >= 1) return 1;
		return t * t * (3 - 2 * t);
	}

	// One hand's state. Call Update once per rendered frame with the live pose; `shown` is what
	// the gun is drawn (and fired) at.
	struct Glide
	{
		bool started = false;
		double stepStart = 0;	// seconds
		Pose from{}, target{}, shown{};

		void Reset() { started = false; }

		const Pose& Update(const Pose& live, double nowSeconds, int stepsPerSecond, int glidePercent)
		{
			if (stepsPerSecond < kMinStepsPerSecond) stepsPerSecond = kMinStepsPerSecond;
			if (stepsPerSecond > kMaxStepsPerSecond) stepsPerSecond = kMaxStepsPerSecond;
			if (glidePercent < kMinGlidePercent) glidePercent = kMinGlidePercent;
			if (glidePercent > 100) glidePercent = 100;
			const double step = 1.0 / stepsPerSecond;
			const double since = nowSeconds - stepStart;

			if (!started || since < 0 || since > kStaleSeconds)
			{
				// first frame, the clock went backwards, or a long pause: no glide to make up
				started = true;
				from = target = shown = live;
				stepStart = nowSeconds;
				return shown;
			}
			if (since >= step)
			{
				// a new step: leave from wherever the gun is drawn right now, head for the hand
				from = shown;
				target = live;
				// keep the rhythm even when frames do not land exactly on the step
				stepStart = (since < 2 * step) ? stepStart + step : nowSeconds;
			}
			const double t = (nowSeconds - stepStart) / (step * glidePercent / 100.0);
			shown = Blend(from, target, Ease(t));
			return shown;
		}
	};
}
