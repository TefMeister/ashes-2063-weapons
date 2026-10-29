// body_rig.h -- a body for the player: where every part of it is, on every rendered frame (2026-10-29, /pd)
//
// Pure maths, plain doubles, no GZDoom and no OpenVR types, so engine/body_rig_test.cpp can compile
// and run THIS FILE on a machine with no engine source and no headset. The engine calls update()
// once per rendered frame and does nothing else with the numbers but draw them, so what the test
// checks is what ships. Same shape as two_handed_aim.h / two_handed_pose.h beside it.
//
// THE PROBLEM. In the headset the player is a camera and two gloves. Tefa asked for a body under
// the camera and arms running from the gloves to the shoulders (body/README.md), mechanics first,
// looks later. Only three things are ever tracked -- the head and the two hands -- so everything
// else is GUESSED from them, every frame, the way every VR game with a body does it:
//
//   head  ->  neck  ->  shoulders  ->  (two-bone IK to each controller)  ->  elbows
//         ->  torso ->  hips       ->  (two-bone IK down to the floor)    ->  knees, ankles
//
// Everything here is in OpenVR's absolute tracking space: right-handed, metres, +Y up, and a
// frame's FORWARD is its -Z (the direction a controller points out of its front). The engine turns
// each part's pose into GZDoom's world with the very same chain a real controller goes through
// (OpenVRMode::GetPoseTransform), so a part is drawn exactly where a controller held there would be.
//
// A PART'S OWN FRAME, which the model files are built against (body/build_body_test.py):
//   LIMBS (upper arm, forearm, thigh, shin): origin at the upper joint (shoulder, elbow, hip, knee);
//     -Z along the limb towards the next joint; +Y the side the up-hint points to (the front of a
//     leg, the back of a hand for a forearm); +X the right-handed completion.
//   TORSO and HIPS: origin at the neck base / the hip centre; -Z the body's forward, +Y up, +X the
//     body's right. They hang DOWN from their origin, along -Y.
//
// ⚠️ WHAT IS NOT ESTABLISHED. Nothing here has been run in the game or worn. Every length below is
// an average adult's for a 1.75 m player, scaled by the player's height, and every one is a guess
// until someone stands in the headset and says the elbow is in the wrong place. They are settings
// (Params), not constants, for exactly that reason. [hypothesis]
#pragma once
#include <cmath>

namespace brg {

constexpr double kPi = 3.14159265358979323846;
constexpr double kDefaultHeight = 1.75;   // metres; every measurement in Params is for a player this tall

enum Part { None = 0, Torso, Hips, UpperArmL, ForearmL, UpperArmR, ForearmR, ThighL, ShinL, ThighR, ShinR, kPartCount };
enum Side { Left = 0, Right = 1 };        // OpenVR's controller roles: 0 = left hand, 1 = right hand

inline const char* part_name(int p)
{
	static const char* names[kPartCount] = { "none", "torso", "hips", "upper arm L", "forearm L", "upper arm R",
		"forearm R", "thigh L", "shin L", "thigh R", "shin R" };
	return (p > 0 && p < kPartCount) ? names[p] : "?";
}

struct Vec { double x, y, z; };
inline Vec vec(double x, double y, double z) { Vec r; r.x = x; r.y = y; r.z = z; return r; }
inline Vec operator+(Vec a, Vec b) { return vec(a.x + b.x, a.y + b.y, a.z + b.z); }
inline Vec operator-(Vec a, Vec b) { return vec(a.x - b.x, a.y - b.y, a.z - b.z); }
inline Vec operator*(Vec a, double s) { return vec(a.x * s, a.y * s, a.z * s); }
inline double dot(Vec a, Vec b) { return a.x * b.x + a.y * b.y + a.z * b.z; }
inline Vec cross(Vec a, Vec b) { return vec(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x); }
inline double len(Vec a) { return std::sqrt(dot(a, a)); }
inline Vec unit(Vec a) { double l = len(a); return l > 1e-12 ? a * (1.0 / l) : vec(0, 0, 0); }   // zero stays zero
inline Vec horizontal(Vec a) { return vec(a.x, 0, a.z); }

struct Basis { Vec x, y, z; };            // the columns of a rotation: where the frame's local axes point
struct Pose { bool valid; Vec pos; Basis b; };

inline Basis identity_basis() { Basis b; b.x = vec(1, 0, 0); b.y = vec(0, 1, 0); b.z = vec(0, 0, 1); return b; }
inline Vec forward_of(const Basis& b) { return b.z * -1.0; }

struct Hand { bool valid; Vec pos; Basis b; };

struct Input {
	Vec head_pos;       // the HMD's own origin (between the eyes, in front of the head's centre)
	Basis head;         // the HMD's frame: -Z where the face points, +Y out of the top of the head
	Hand hand[2];       // [Left], [Right]; valid = tracked this frame
	double floor_y;     // tracking-space height of the real floor (vr_floor_offset)
	// How the player is moving through the level (stick walking, not real-room steps): the legs step
	// with it (Tefa, 2026-10-29: "legs animating with player speed"). speed in m/s; move_dir a
	// horizontal unit vector in tracking space (anything when speed is 0).
	double speed;
	Vec move_dir;
};

// Every number is for a kDefaultHeight player and is multiplied by height / kDefaultHeight.
struct Params {
	double height = kDefaultHeight;      // the player's height in metres (vr_body_height)
	// head and neck
	double head_centre_back = 0.08;      // the HMD origin sits this far in front of the head's centre
	double neck_below_head  = 0.12;      // head centre to the base of the neck (the point the head turns about)
	// shoulders
	double shoulder_half_width = 0.19;   // neck to each shoulder joint, sideways
	double shoulder_below_neck = 0.04;
	// arms
	double upper_arm = 0.32;             // shoulder joint to elbow
	double forearm   = 0.27;             // elbow to wrist
	double wrist_back_of_controller = 0.06;   // the controller's origin is in the palm; the wrist is behind it...
	double wrist_below_controller   = 0.02;   // ...and a little below it
	double elbow_out  = 0.6;             // where the elbow bends to, as a direction in the body's frame:
	double elbow_down = 1.0;             //   out to the side, down, and back. Shape only; it is normalised.
	double elbow_back = 0.3;
	// torso and legs
	double torso_length   = 0.55;        // neck base to hip centre
	double hip_half_width = 0.10;        // hip centre to each hip joint
	double thigh = 0.45;                 // hip joint to knee
	double shin  = 0.45;                 // knee to ankle
	double ankle_above_floor = 0.08;
	// how the body turns after the head
	double yaw_deadzone_deg = 25.0;      // a glance this far to the side does not swing the chest
	double yaw_rate = 4.0;               // per second; how fast the chest catches up once outside the dead zone
	double hand_yaw_weight = 0.5;        // the chest also turns towards where the hands are (0 = head only)
	double hand_yaw_min_reach = 0.15;    // hands closer than this to the body's axis say nothing about its facing
	double hand_yaw_max_deg = 90.0;      // hands further round than this (behind the back) are ignored
	// walking: the feet step along the direction of travel, one after the other
	double stride = 0.65;                // metres covered by one full step cycle (both feet) at full amplitude
	double step_height = 0.08;           // how high a swinging foot lifts
	double walk_full_speed = 1.2;        // m/s at which the steps reach their full length
	double walk_min_speed = 0.1;         // below this the player is standing: the feet settle under the hips
	double walk_settle_rate = 6.0;       // per second; how fast the steps fade in and out and the feet settle
};

struct State {
	bool started = false;
	double body_yaw = 0.0;               // degrees; 0 = facing -Z, positive = turned to the left
	double walk_phase = 0.0;             // step cycles; the left foot is forward at 0, the right at 0.5
	double walk_amp = 0.0;               // 0 = standing, 1 = full stride
};

struct Rig {
	Pose parts[kPartCount];
	double body_yaw = 0.0;
	Vec body_forward, body_right;        // horizontal unit vectors
	Vec neck, hip_centre;
	Vec shoulder[2], elbow[2], wrist[2]; // [Left], [Right]
	Vec hip[2], knee[2], ankle[2];
	bool arm_straight[2];                // the controller was out of reach; the forearm points at it and stops short
	double walk_phase = 0.0, walk_amp = 0.0;
	double foot_lift[2];                 // how high each foot is off the floor this frame
};

inline double wrap_deg(double a) { while (a > 180.0) a -= 360.0; while (a <= -180.0) a += 360.0; return a; }
// Yaw of a horizontal direction: 0 facing -Z, +90 facing -X (to the left; right-handed about +Y).
inline double yaw_of(Vec fwd) { return std::atan2(-fwd.x, -fwd.z) * (180.0 / kPi); }
inline Vec forward_from_yaw(double yaw_deg) { double r = yaw_deg * kPi / 180.0; return vec(-std::sin(r), 0, -std::cos(r)); }
inline Vec right_from_yaw(double yaw_deg)   { double r = yaw_deg * kPi / 180.0; return vec(std::cos(r), 0, -std::sin(r)); }

// A limb's frame: origin `from`, -Z pointing at `to`, +Y the up-hint made perpendicular (the fallback
// when the hint lies along the limb), +X completing a right-handed frame.
inline Basis limb_basis(Vec from, Vec to, Vec up_hint, Vec up_fallback)
{
	Vec fwd = unit(to - from);
	Vec y = up_hint - fwd * dot(up_hint, fwd);
	if (len(y) < 1e-6) y = up_fallback - fwd * dot(up_fallback, fwd);
	if (len(y) < 1e-6) y = cross(fwd, vec(1, 0, 0));            // both hints along the limb: anything perpendicular
	Basis b;
	b.z = fwd * -1.0;
	b.y = unit(y);
	b.x = cross(b.y, b.z);
	return b;
}

// Two-bone IK: a joint at S, a bone of length L1 to the middle joint, a bone of length L2 to the
// target T. Returns the middle joint, bent towards `pole` (the side the elbow / knee goes). Out of
// reach: the first bone points straight at T (`*straight` = true), the second will stop short.
inline Vec two_bone(Vec S, Vec T, double L1, double L2, Vec pole, Vec pole_fallback, bool* straight)
{
	*straight = false;
	Vec d = T - S;
	double dist = len(d);
	if (dist < 1e-9) return S + unit(pole) * L1;                 // target on the joint itself: fold along the pole
	Vec axis = d * (1.0 / dist);
	double a, h;
	if (dist >= L1 + L2) { a = L1; h = 0.0; *straight = true; }
	else
	{
		a = (L1 * L1 - L2 * L2 + dist * dist) / (2.0 * dist);
		if (a > L1) a = L1;
		if (a < -L1) a = -L1;
		h = std::sqrt(L1 * L1 - a * a);
	}
	Vec perp = pole - axis * dot(pole, axis);
	if (len(perp) < 1e-6) perp = pole_fallback - axis * dot(pole_fallback, axis);
	if (len(perp) < 1e-6) perp = cross(axis, vec(1, 0, 0));
	return S + axis * a + unit(perp) * h;
}

// Where the chest faces this frame, from where it faced last frame, the head and the hands.
inline double follow_yaw(const State& st, double head_yaw, bool hands_known, double hands_yaw, const Params& p, double dt)
{
	double target = head_yaw;
	if (hands_known)
	{
		double off = wrap_deg(hands_yaw - head_yaw);
		if (std::fabs(off) <= p.hand_yaw_max_deg) target = head_yaw + p.hand_yaw_weight * off;
	}
	if (!st.started) return wrap_deg(target);
	double diff = wrap_deg(target - st.body_yaw);
	if (std::fabs(diff) <= p.yaw_deadzone_deg) return st.body_yaw;
	double overshoot = diff - (diff > 0 ? p.yaw_deadzone_deg : -p.yaw_deadzone_deg);  // how far outside the dead zone
	double k = 1.0 - std::exp(-p.yaw_rate * (dt > 0 ? dt : 0));
	return wrap_deg(st.body_yaw + overshoot * k);
}

inline void update(const Input& in, const Params& p, double dt, State& st, Rig& out)
{
	const double s = p.height / kDefaultHeight;
	const Vec up = vec(0, 1, 0);
	const Vec down = vec(0, -1, 0);

	// 1. The neck: behind and below the HMD, along the head's own axes, so it stays put when the head nods.
	const Vec head_fwd = forward_of(in.head);
	const Vec head_centre = in.head_pos - head_fwd * (p.head_centre_back * s);
	out.neck = head_centre - in.head.y * (p.neck_below_head * s);

	// 2. Which way the body faces.
	const double head_yaw = yaw_of(horizontal(head_fwd));
	bool hands_known = in.hand[Left].valid && in.hand[Right].valid;
	double hands_yaw = head_yaw;
	if (hands_known)
	{
		Vec mid = (in.hand[Left].pos + in.hand[Right].pos) * 0.5;
		Vec reach = horizontal(mid - out.neck);
		if (len(reach) >= p.hand_yaw_min_reach * s) hands_yaw = yaw_of(reach);
		else hands_known = false;
	}
	out.body_yaw = follow_yaw(st, head_yaw, hands_known, hands_yaw, p, dt);
	st.body_yaw = out.body_yaw;
	st.started = true;
	out.body_forward = forward_from_yaw(out.body_yaw);
	out.body_right = right_from_yaw(out.body_yaw);
	Basis body;
	body.x = out.body_right; body.y = up; body.z = out.body_forward * -1.0;

	// 3. Walking: a step cycle that runs with the player's speed and fades out when they stand.
	//    Each foot swings forward along the direction of travel, lifted while it swings, and then
	//    stays planted while the body carries on past it (so, relative to the hips, it slides back).
	const double k_settle = 1.0 - std::exp(-p.walk_settle_rate * (dt > 0 ? dt : 0));
	const bool walking = in.speed >= p.walk_min_speed;
	const double amp_target = walking ? (in.speed / p.walk_full_speed > 1.0 ? 1.0 : in.speed / p.walk_full_speed) : 0.0;
	st.walk_amp += (amp_target - st.walk_amp) * k_settle;
	if (walking)
	{
		st.walk_phase += in.speed * (dt > 0 ? dt : 0) / (p.stride * s);
		st.walk_phase -= std::floor(st.walk_phase);
	}
	else
	{
		// settle on the nearest rest point (0 or 0.5: with the amplitude fading, both feet end under the hips)
		double rest = std::floor(st.walk_phase * 2.0 + 0.5) / 2.0;
		st.walk_phase += (rest - st.walk_phase) * k_settle;
	}
	out.walk_phase = st.walk_phase;
	out.walk_amp = st.walk_amp;
	Vec travel = horizontal(in.move_dir);
	travel = len(travel) > 1e-6 ? unit(travel) : out.body_forward;
	const double along_max = out.walk_amp * (p.stride * s) * 0.5;   // the furthest a foot gets from under its hip

	// 4. Torso and hips hang from the neck. If the legs cannot reach the floor the hips come down to
	//    where they can (the torso stretches a little rather than the feet floating); mid-stride that
	//    is a little lower still, so the foot swung out in front can still be reached.
	out.parts[Torso].valid = true; out.parts[Torso].pos = out.neck; out.parts[Torso].b = body;
	out.hip_centre = out.neck + down * (p.torso_length * s);
	const double leg_len = (p.thigh + p.shin) * s;
	const double leg_reach = std::sqrt(leg_len * leg_len - along_max * along_max) + p.ankle_above_floor * s;
	if (out.hip_centre.y - in.floor_y > leg_reach) out.hip_centre.y = in.floor_y + leg_reach;
	out.parts[Hips].valid = true; out.parts[Hips].pos = out.hip_centre; out.parts[Hips].b = body;

	// 5. Arms: shoulder to the controller, elbow out, down and back.
	for (int side = 0; side < 2; ++side)
	{
		const double sgn = (side == Right) ? 1.0 : -1.0;
		out.shoulder[side] = out.neck + out.body_right * (sgn * p.shoulder_half_width * s) + down * (p.shoulder_below_neck * s);
		const Hand& h = in.hand[side];
		Vec hand_up = up;
		if (h.valid)
		{
			out.wrist[side] = h.pos + h.b.z * (p.wrist_back_of_controller * s) - h.b.y * (p.wrist_below_controller * s);
			hand_up = h.b.y;
		}
		else
		{
			// Not tracked: the arm hangs by the side, a little forward, so the sleeve does not vanish.
			out.wrist[side] = out.shoulder[side] + down * ((p.upper_arm + p.forearm) * s) + out.body_forward * (0.05 * s);
		}
		Vec pole = out.body_right * (sgn * p.elbow_out) + down * p.elbow_down - out.body_forward * p.elbow_back;
		out.elbow[side] = two_bone(out.shoulder[side], out.wrist[side], p.upper_arm * s, p.forearm * s, pole, down, &out.arm_straight[side]);
		const int ua = (side == Right) ? UpperArmR : UpperArmL;
		const int fa = (side == Right) ? ForearmR : ForearmL;
		out.parts[ua].valid = true; out.parts[ua].pos = out.shoulder[side];
		out.parts[ua].b = limb_basis(out.shoulder[side], out.elbow[side], up, out.body_forward * -1.0);
		out.parts[fa].valid = true; out.parts[fa].pos = out.elbow[side];
		out.parts[fa].b = limb_basis(out.elbow[side], out.wrist[side], hand_up, up);
	}

	// 6. Legs: each hip down to its foot target, knees bending forward when the hips are low (crouching).
	for (int side = 0; side < 2; ++side)
	{
		const double sgn = (side == Right) ? 1.0 : -1.0;
		out.hip[side] = out.hip_centre + out.body_right * (sgn * p.hip_half_width * s);
		const double phase = out.walk_phase + (side == Right ? 0.5 : 0.0);
		const double along = out.walk_amp * (p.stride * s) * 0.5 * std::cos(2.0 * kPi * phase);
		const double swing = -std::sin(2.0 * kPi * phase);                  // > 0 while this foot moves forward
		out.foot_lift[side] = out.walk_amp * (p.step_height * s) * (swing > 0 ? swing : 0.0);
		out.ankle[side] = vec(out.hip[side].x, in.floor_y + p.ankle_above_floor * s, out.hip[side].z)
			+ travel * along + up * out.foot_lift[side];
		bool straight;
		out.knee[side] = two_bone(out.hip[side], out.ankle[side], p.thigh * s, p.shin * s, out.body_forward, out.body_right, &straight);
		const int th = (side == Right) ? ThighR : ThighL;
		const int sh = (side == Right) ? ShinR : ShinL;
		out.parts[th].valid = true; out.parts[th].pos = out.hip[side];
		out.parts[th].b = limb_basis(out.hip[side], out.knee[side], out.body_forward, out.body_right);
		out.parts[sh].valid = true; out.parts[sh].pos = out.knee[side];
		out.parts[sh].b = limb_basis(out.knee[side], out.ankle[side], out.body_forward, out.body_right);
	}
	out.parts[None].valid = false;
}

} // namespace brg
