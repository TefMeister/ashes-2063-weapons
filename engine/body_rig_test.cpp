// body_rig_test.cpp -- numeric checks of body_rig.h, no engine, no headset (2026-10-29, /pd).
// Build and run: engine\run_body_rig_test.bat. Every check prints PASS or FAIL; the exit code is the
// number of failures. `--dump` also prints every part's pose for the standing case.
#include "body_rig.h"
#include <cstdio>
#include <cstring>
#include <cmath>

using namespace brg;

static int failures = 0;
static void check(bool ok, const char* what)
{
	std::printf("%s  %s\n", ok ? "PASS" : "FAIL", what);
	if (!ok) ++failures;
}
static bool near(double a, double b, double tol) { return std::fabs(a - b) <= tol; }
static bool near_v(Vec a, Vec b, double tol) { return len(a - b) <= tol; }

static double det(const Basis& b)
{
	return dot(b.x, cross(b.y, b.z));
}
static bool orthonormal_right_handed(const Basis& b, double tol)
{
	return near(len(b.x), 1, tol) && near(len(b.y), 1, tol) && near(len(b.z), 1, tol)
		&& near(dot(b.x, b.y), 0, tol) && near(dot(b.y, b.z), 0, tol) && near(dot(b.x, b.z), 0, tol)
		&& near(det(b), 1, tol);
}

// A frame facing `yaw_deg` (0 = -Z), upright: -Z forward, +Y up, +X right.
static Basis facing(double yaw_deg)
{
	Basis b;
	b.z = forward_from_yaw(yaw_deg) * -1.0;
	b.y = vec(0, 1, 0);
	b.x = cross(b.y, b.z);
	return b;
}

static Hand hand_at(double x, double y, double z, bool valid = true)
{
	Hand h; h.valid = valid; h.pos = vec(x, y, z); h.b = identity_basis(); return h;
}

// The standing reference: 1.65 m eye height, facing -Z, hands held in front at hip height.
static Input standing()
{
	Input in;
	in.head_pos = vec(0, 1.65, 0);
	in.head = identity_basis();
	in.hand[Left] = hand_at(-0.22, 1.10, -0.22);
	in.hand[Right] = hand_at(0.22, 1.10, -0.22);
	in.floor_y = 0;
	in.speed = 0;
	in.move_dir = vec(0, 0, -1);
	return in;
}

static void dump(const Rig& r)
{
	std::printf("body yaw %.1f deg, neck (%.3f %.3f %.3f), hips (%.3f %.3f %.3f)\n", r.body_yaw,
		r.neck.x, r.neck.y, r.neck.z, r.hip_centre.x, r.hip_centre.y, r.hip_centre.z);
	for (int i = 1; i < kPartCount; ++i)
	{
		const Pose& p = r.parts[i];
		std::printf("  %-12s at (%6.3f %6.3f %6.3f)  fwd (%5.2f %5.2f %5.2f)  up (%5.2f %5.2f %5.2f)\n", part_name(i),
			p.pos.x, p.pos.y, p.pos.z, -p.b.z.x, -p.b.z.y, -p.b.z.z, p.b.y.x, p.b.y.y, p.b.y.z);
	}
}

int main(int argc, char** argv)
{
	const bool want_dump = argc > 1 && std::strcmp(argv[1], "--dump") == 0;
	Params p;
	const double s = p.height / kDefaultHeight;   // 1 for the defaults
	const double tol = 1e-9;

	// ---- 1. the standing case
	{
		State st; Rig r;
		Input in = standing();
		update(in, p, 1.0 / 90, st, r);
		if (want_dump) dump(r);

		bool all_valid = true, all_frames = true;
		for (int i = 1; i < kPartCount; ++i)
		{
			all_valid = all_valid && r.parts[i].valid;
			all_frames = all_frames && orthonormal_right_handed(r.parts[i].b, 1e-9);
		}
		check(all_valid, "standing: every part has a pose");
		check(all_frames, "standing: every part's frame is orthonormal and right-handed (det +1)");
		// facing -Z, "behind" is +Z
		check(near_v(r.neck, vec(0, 1.65 - p.neck_below_head, p.head_centre_back), tol), "standing: the neck is 12 cm below and 8 cm behind the HMD");
		check(near(r.body_yaw, 0, tol), "standing: body faces the way the head faces");
		check(near_v(r.body_forward, vec(0, 0, -1), tol) && near_v(r.body_right, vec(1, 0, 0), tol), "standing: body forward is -Z, right is +X");

		// arms
		for (int side = 0; side < 2; ++side)
		{
			char buf[160];
			const double lu = len(r.elbow[side] - r.shoulder[side]);
			const double lf = len(r.wrist[side] - r.elbow[side]);
			std::snprintf(buf, sizeof buf, "standing: %s arm bones keep their lengths (%.4f / %.4f)", side ? "right" : "left", lu, lf);
			check(near(lu, p.upper_arm * s, tol) && near(lf, p.forearm * s, tol) && !r.arm_straight[side], buf);
			// the elbow is below the shoulder-wrist line and out to its own side
			Vec axis = unit(r.wrist[side] - r.shoulder[side]);
			Vec e_rel = r.elbow[side] - r.shoulder[side];
			Vec perp = e_rel - axis * dot(e_rel, axis);
			std::snprintf(buf, sizeof buf, "standing: %s elbow bends down and outward (perp y %.3f, x %.3f)", side ? "right" : "left", perp.y, perp.x);
			check(perp.y < 0 && (side == Right ? perp.x > 0 : perp.x < 0), buf);
			// the wrist sits behind and below the controller
			Vec expect_w = (side == Right ? vec(0.22, 1.10, -0.22) : vec(-0.22, 1.10, -0.22)) + vec(0, -p.wrist_below_controller, p.wrist_back_of_controller);
			std::snprintf(buf, sizeof buf, "standing: %s wrist is 6 cm behind and 2 cm below the controller", side ? "right" : "left");
			check(near_v(r.wrist[side], expect_w, tol), buf);
			// the upper arm part starts at the shoulder and points at the elbow; the forearm starts at the elbow and points at the wrist
			const int ua = side ? UpperArmR : UpperArmL, fa = side ? ForearmR : ForearmL;
			check(near_v(r.parts[ua].pos, r.shoulder[side], tol) && near_v(forward_of(r.parts[ua].b), unit(r.elbow[side] - r.shoulder[side]), tol),
				"standing: upper arm part sits on the shoulder and points at the elbow");
			check(near_v(r.parts[fa].pos, r.elbow[side], tol) && near_v(forward_of(r.parts[fa].b), unit(r.wrist[side] - r.elbow[side]), tol),
				"standing: forearm part sits on the elbow and points at the wrist");
		}
		// left/right symmetry of the whole standing pose
		check(near(r.elbow[Left].x, -r.elbow[Right].x, tol) && near(r.elbow[Left].y, r.elbow[Right].y, tol) && near(r.elbow[Left].z, r.elbow[Right].z, tol),
			"standing: the elbows mirror each other");
		check(near(r.shoulder[Right].x - r.shoulder[Left].x, 2 * p.shoulder_half_width * s, tol), "standing: shoulders are 38 cm apart");

		// legs: feet on the floor under the hips, legs nearly straight, hips where the legs reach
		const double leg_reach = (p.thigh + p.shin + p.ankle_above_floor) * s;
		check(near(r.hip_centre.y, leg_reach, tol) || r.hip_centre.y < leg_reach, "standing: the hips are no higher than the legs can reach");
		for (int side = 0; side < 2; ++side)
		{
			check(near(r.ankle[side].y, p.ankle_above_floor * s, tol) && near(r.ankle[side].x, r.hip[side].x, tol) && near(r.ankle[side].z, r.hip[side].z, tol),
				"standing: the foot is on the floor straight under its hip");
			const double lt = len(r.knee[side] - r.hip[side]), ls = len(r.ankle[side] - r.knee[side]);
			check(near(lt, p.thigh * s, tol) && near(ls, p.shin * s, tol), "standing: leg bones keep their lengths");
			// knee in front of the hip-ankle line (bends forward), and only a little when standing tall
			Vec axis = unit(r.ankle[side] - r.hip[side]);
			Vec k_rel = r.knee[side] - r.hip[side];
			Vec perp = k_rel - axis * dot(k_rel, axis);
			check(dot(perp, r.body_forward) >= -tol, "standing: the knee bends forward, never backward");
		}
	}

	// ---- 2. crouching: the head comes down 45 cm, the knees must bend forward and the feet stay down
	{
		State st; Rig r;
		Input in = standing();
		in.head_pos.y = 1.20;
		update(in, p, 1.0 / 90, st, r);
		for (int side = 0; side < 2; ++side)
		{
			Vec axis = unit(r.ankle[side] - r.hip[side]);
			Vec k_rel = r.knee[side] - r.hip[side];
			Vec perp = k_rel - axis * dot(k_rel, axis);
			char buf[120];
			std::snprintf(buf, sizeof buf, "crouching: the knee is well forward of the hip-ankle line (%.3f m)", dot(perp, r.body_forward));
			check(dot(perp, r.body_forward) > 0.10, buf);
			check(near(r.ankle[side].y, p.ankle_above_floor * s, tol), "crouching: the foot stays on the floor");
			check(near(len(r.knee[side] - r.hip[side]), p.thigh * s, tol) && near(len(r.ankle[side] - r.knee[side]), p.shin * s, tol), "crouching: leg bones keep their lengths");
		}
		check(near(r.hip_centre.y, 1.20 - p.neck_below_head - p.torso_length, tol), "crouching: the hips hang the torso's length below the neck");
	}

	// ---- 3. nodding: the neck is the pivot, so it barely moves when the head looks down 45 degrees
	{
		State st; Rig up_r, down_r;
		Input in = standing();
		update(in, p, 1.0 / 90, st, up_r);
		// head pitched 45 deg down about the neck: the HMD swings forward and down
		const double a = 45 * kPi / 180;
		Basis h; h.x = vec(1, 0, 0); h.y = vec(0, std::cos(a), -std::sin(a)); h.z = vec(0, std::sin(a), std::cos(a));
		// the head's centre stays where it was; the HMD origin is 8 cm in front of it, along the new forward
		Vec centre = vec(0, 1.65, p.head_centre_back);
		Vec neck_true = centre - vec(0, p.neck_below_head, 0);
		// rotate the centre about the neck too (that is what a real nod does)
		Vec c_rel = centre - neck_true;
		Vec c_new = neck_true + h.x * c_rel.x + h.y * c_rel.y + h.z * c_rel.z;
		Input down = standing();
		down.head = h;
		down.head_pos = c_new + forward_of(h) * p.head_centre_back;
		State st2;
		update(down, p, 1.0 / 90, st2, down_r);
		char buf[120];
		std::snprintf(buf, sizeof buf, "nodding 45 deg down: the neck stays put (moved %.4f m)", len(down_r.neck - up_r.neck));
		check(near_v(down_r.neck, up_r.neck, 1e-9), buf);
	}

	// ---- 4. the body follows the head only outside the dead zone
	{
		State st; Rig r;
		Input in = standing();
		in.hand[Left].valid = in.hand[Right].valid = false;     // head only, for this check
		update(in, p, 1.0 / 90, st, r);
		// a 15 degree glance: inside the 25 degree dead zone, the chest does not move at all over a full second
		in.head = facing(15);
		for (int i = 0; i < 90; ++i) update(in, p, 1.0 / 90, st, r);
		check(near(r.body_yaw, 0, tol), "glance 15 deg: the chest does not move");
		// a 70 degree turn: the chest follows until it is within the dead zone of the head
		in.head = facing(70);
		for (int i = 0; i < 180; ++i) update(in, p, 1.0 / 90, st, r);
		char buf[120];
		std::snprintf(buf, sizeof buf, "turn 70 deg: after 2 s the chest is %.1f deg round (dead zone 25)", r.body_yaw);
		check(r.body_yaw > 70 - p.yaw_deadzone_deg - 0.5 && r.body_yaw <= 70 - p.yaw_deadzone_deg + 1e-6, buf);
		// across the +-180 seam: facing 170 then turning to -170 must move 20 degrees, not 340
		State st3; Rig r3;
		in.head = facing(170);
		update(in, p, 1.0 / 90, st3, r3);
		in.head = facing(-170);
		for (int i = 0; i < 90; ++i) update(in, p, 1.0 / 90, st3, r3);
		check(near(r3.body_yaw, 170, tol), "seam: a 20 deg turn across +-180 stays inside the dead zone");
		// with the hands held out to the left, the chest turns part way towards them (hand weight 0.5)
		State st4; Rig r4;
		Input hands = standing();
		hands.hand[Left] = hand_at(-0.6, 1.0, 0.0);
		hands.hand[Right] = hand_at(-0.6, 1.0, -0.2);
		update(hands, p, 1.0 / 90, st4, r4);
		check(r4.body_yaw > 20 && r4.body_yaw < 70, "hands held out to the left: the chest turns part of the way (head stays)");
	}

	// ---- 5. out of reach, and an untracked hand
	{
		State st; Rig r;
		Input in = standing();
		in.hand[Right] = hand_at(1.5, 1.4, -1.5);
		update(in, p, 1.0 / 90, st, r);
		check(r.arm_straight[Right], "out of reach: the right arm is reported straight");
		Vec axis = unit(r.wrist[Right] - r.shoulder[Right]);
		check(near_v(r.elbow[Right], r.shoulder[Right] + axis * (p.upper_arm * s), tol), "out of reach: the elbow is one upper arm along the line to the hand");
		check(near_v(forward_of(r.parts[ForearmR].b), axis, tol), "out of reach: the forearm points at the hand");
		in = standing();
		in.hand[Left].valid = false;
		State st2; Rig r2;
		update(in, p, 1.0 / 90, st2, r2);
		check(r2.parts[UpperArmL].valid && r2.parts[ForearmL].valid, "left hand not tracked: the left sleeve still has a pose");
		check(r2.wrist[Left].y < r2.shoulder[Left].y - 0.5, "left hand not tracked: the arm hangs down");
	}

	// ---- 6. walking: the feet step with the speed, alternate, never go through the floor, and settle when stopping
	{
		State st; Rig r;
		Input in = standing();
		in.speed = 1.2;             // full stride
		in.move_dir = vec(0, 0, -1);
		const double dt = 1.0 / 90;
		double max_lift[2] = { 0, 0 };
		bool floor_ok = true, lengths_ok = true, alternate_ok = true;
		int both_up = 0, samples = 0;
		for (int i = 0; i < 270; ++i)      // 3 seconds
		{
			update(in, p, dt, st, r);
			for (int side = 0; side < 2; ++side)
			{
				if (r.foot_lift[side] > max_lift[side]) max_lift[side] = r.foot_lift[side];
				if (r.ankle[side].y < p.ankle_above_floor * s - 1e-9) floor_ok = false;
				if (!near(len(r.knee[side] - r.hip[side]), p.thigh * s, tol) || !near(len(r.ankle[side] - r.knee[side]), p.shin * s, tol)) lengths_ok = false;
			}
			if (i > 90) { ++samples; if (r.foot_lift[Left] > 1e-6 && r.foot_lift[Right] > 1e-6) ++both_up; }
		}
		alternate_ok = both_up == 0;
		char buf[160];
		std::snprintf(buf, sizeof buf, "walking 1.2 m/s: phase advanced %.2f cycles in 3 s (expect %.2f)", st.walk_phase + std::floor(3.0 * 1.2 / p.stride), 3.0 * 1.2 / p.stride);
		// 3 s * 1.2 m/s / 0.65 m = 5.538 cycles -> fractional part 0.538
		check(near(st.walk_phase, std::fmod(3.0 * 1.2 / (p.stride * s), 1.0), 1e-6), buf);
		std::snprintf(buf, sizeof buf, "walking: both feet lift to the step height (%.3f / %.3f, expect %.3f)", max_lift[Left], max_lift[Right], p.step_height * s);
		check(near(max_lift[Left], p.step_height * s, 0.005) && near(max_lift[Right], p.step_height * s, 0.005), buf);
		check(floor_ok, "walking: no foot ever goes below the floor");
		check(lengths_ok, "walking: leg bones keep their lengths through the whole cycle");
		check(alternate_ok, "walking: the two feet are never in the air at the same time");
		check(near(r.walk_amp, 1.0, 1e-3), "walking: the stride reaches full amplitude");
		// the planted foot is behind the hips when the other swings forward (feet spread along the travel line)
		update(in, p, dt, st, r);
		double spread = std::fabs(dot(r.ankle[Left] - r.ankle[Right], in.move_dir));
		std::snprintf(buf, sizeof buf, "walking: the feet are spread along the direction of travel (%.3f m)", spread);
		check(spread > 0.1, buf);
		// stop: within a second the feet are back under the hips and still
		in.speed = 0;
		for (int i = 0; i < 90; ++i) update(in, p, dt, st, r);
		std::snprintf(buf, sizeof buf, "stopping: after 1 s the feet are under the hips again (amp %.4f, lift %.4f)", r.walk_amp, r.foot_lift[Left] + r.foot_lift[Right]);
		check(r.walk_amp < 0.01 && r.foot_lift[Left] + r.foot_lift[Right] < 0.001, buf);
		// a slow shuffle steps shorter, not faster
		State st2; Rig r2; Input slow = standing(); slow.speed = 0.4;
		for (int i = 0; i < 270; ++i) update(slow, p, dt, st2, r2);
		std::snprintf(buf, sizeof buf, "walking 0.4 m/s: shorter steps (amp %.2f) at the same metres-per-cycle", r2.walk_amp);
		check(near(r2.walk_amp, 0.4 / 1.2, 1e-3) && near(st2.walk_phase, std::fmod(3.0 * 0.4 / (p.stride * s), 1.0), 1e-6), buf);
		// walking sideways: the feet spread along the travel line, not the body's forward
		State st3; Rig r3; Input side = standing(); side.speed = 1.2; side.move_dir = vec(1, 0, 0);
		for (int i = 0; i < 100; ++i) update(side, p, dt, st3, r3);
		double sx = std::fabs(r3.ankle[Left].x - r3.ankle[Right].x) - 2 * p.hip_half_width * s;
		double sz = std::fabs(r3.ankle[Left].z - r3.ankle[Right].z);
		check(std::fabs(sx) > 0.05 && sz < 1e-9, "strafing right: the feet step sideways, not forward");
	}

	// ---- 7. a taller player: everything scales
	{
		Params tall = p; tall.height = 1.95;
		State st; Rig r;
		Input in = standing(); in.head_pos.y = 1.85;
		update(in, tall, 1.0 / 90, st, r);
		const double ts = 1.95 / kDefaultHeight;
		check(near(len(r.elbow[Right] - r.shoulder[Right]), p.upper_arm * ts, tol), "1.95 m player: the upper arm is scaled up");
		check(near(r.shoulder[Right].x - r.shoulder[Left].x, 2 * p.shoulder_half_width * ts, tol), "1.95 m player: the shoulders are wider");
	}

	std::printf("\n%d failure(s)\n", failures);
	return failures;
}
