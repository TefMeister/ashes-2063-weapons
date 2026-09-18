// two_handed_aim_test.cpp -- does the two-hand aim line point where a person would say it does?
// Build + run (MSVC):  cl /nologo /EHsc /W3 /std:c++17 two_handed_aim_test.cpp && two_handed_aim_test.exe
//            (gcc):    g++ -O2 -std=c++17 -o two_handed_aim_test two_handed_aim_test.cpp && ./two_handed_aim_test
// C++17 is not a whim: the header uses `inline constexpr` for the two named limits, which is what
// lets the engine and this test share one definition of them. GZDoom already builds at C++17.
//
// This compiles the SHIPPED header, not a copy of it, so a change to engine/two_handed_aim.h that
// breaks a case shows up here. Ground truth is built independently: each case states the hand
// positions in plain geometry (due north, 30 degrees up, and so on) and asserts the angle a person
// would read off, rather than re-deriving it with the same formula under test.
//
// The sign conventions being pinned are GZDoom's, taken from the off-hand block of our own engine
// patch: world space is X east, Y north, Z up; yaw is atan2(north, east) so 0 = east and +90 = north;
// PITCH IS POSITIVE DOWNWARD. Getting the pitch sign backwards is the single most likely mistake
// here and it would look plausible in a headset -- the gun would simply shoot high when aimed low.
#include "two_handed_aim.h"
#include <cstdio>
#include <cmath>

static int g_fail = 0;
static int g_checks = 0;

static void check(bool cond, const char* what) {
    ++g_checks;
    if (!cond) { ++g_fail; std::printf("  FAIL: %s\n", what); }
}

static void near_deg(double got, double want, const char* what, double tol = 1e-6) {
    ++g_checks;
    // Angles wrap: -180 and +180 are the same bearing, so compare the shortest way round.
    double d = std::fmod(got - want + 540.0, 360.0) - 180.0;
    if (std::fabs(d) > tol) {
        ++g_fail;
        std::printf("  FAIL: %s (got %.6f, want %.6f)\n", what, got, want);
    }
}

static tha::Limits lim() { return tha::Limits{ tha::kMinSeparation, tha::kMaxDisagreeDeg }; }

// Hands a clear 20 map units apart along a direction given in plain geometry, with the weapon
// forward pointing the same way (so guard 2 is satisfied and the case is about the maths).
static tha::Hands along(double dx, double dy, double dz) {
    const double l = std::sqrt(dx * dx + dy * dy + dz * dz);
    const double ux = dx / l, uy = dy / l, uz = dz / l;
    const double sep = 20.0;
    tha::Hands h{};
    h.rear_x = 100.0;  h.rear_y = 200.0;  h.rear_z = 40.0;
    h.front_x = h.rear_x + ux * sep;
    h.front_y = h.rear_y + uy * sep;
    h.front_z = h.rear_z + uz * sep;
    h.fwd_x = ux; h.fwd_y = uy; h.fwd_z = uz;
    return h;
}

int main() {
    std::printf("two-handed aim: where does the gun actually point?\n");

    // ---- 1. THE FOUR COMPASS POINTS, level. Independent ground truth: yaw is atan2(north, east).
    {
        const tha::Aim e = tha::decide(along( 1,  0, 0), lim());
        check(e.use, "due east: accepted");
        near_deg(e.yaw_deg, 0.0, "due east: yaw 0");
        near_deg(e.pitch_deg, 0.0, "due east: level");

        near_deg(tha::decide(along(0,  1, 0), lim()).yaw_deg,  90.0, "due north: yaw +90");
        near_deg(tha::decide(along(-1, 0, 0), lim()).yaw_deg, 180.0, "due west: yaw 180");
        near_deg(tha::decide(along(0, -1, 0), lim()).yaw_deg, -90.0, "due south: yaw -90");
        near_deg(tha::decide(along(1,  1, 0), lim()).yaw_deg,  45.0, "north-east: yaw +45");
    }

    // ---- 2. THE PITCH SIGN. This is the one that would look plausible while being backwards, so
    // it is asserted from the convention rather than from the formula: aiming UP must give a
    // NEGATIVE pitch, because GZDoom counts pitch positive downward.
    {
        // 30 degrees above level: horizontal run 1, rise tan(30).
        const double rise = std::tan(30.0 * 3.14159265358979323846 / 180.0);
        const tha::Aim up = tha::decide(along(1, 0, rise), lim());
        check(up.use, "aimed up: accepted");
        near_deg(up.pitch_deg, -30.0, "aimed 30 up: pitch is -30 (negative = up)", 1e-6);

        const tha::Aim dn = tha::decide(along(1, 0, -rise), lim());
        near_deg(dn.pitch_deg, 30.0, "aimed 30 down: pitch is +30 (positive = down)", 1e-6);

        // Straight up and straight down are the extremes and must not overshoot or NaN.
        const tha::Aim vert = tha::decide(along(0, 0, 1), lim());
        check(vert.use, "straight up: accepted");
        near_deg(vert.pitch_deg, -90.0, "straight up: pitch -90");
        check(!std::isnan(vert.yaw_deg), "straight up: yaw is a number, not NaN");
        near_deg(tha::decide(along(0, 0, -1), lim()).pitch_deg, 90.0, "straight down: pitch +90");
    }

    // ---- 3. GUARD 1: the hands are too close together. A direction from two nearly coincident
    // tracked points is noise, and the honest answer is to leave the aim alone.
    {
        tha::Hands h = along(1, 0, 0);
        h.front_x = h.rear_x + 1.0;   // 1 map unit apart, well under the minimum
        h.front_y = h.rear_y;
        h.front_z = h.rear_z;
        const tha::Aim a = tha::decide(h, lim());
        check(!a.use, "hands together: refuses rather than aiming on noise");
        check(a.sep < tha::kMinSeparation, "hands together: the separation is reported for the log");

        tha::Hands same = along(1, 0, 0);
        same.front_x = same.rear_x; same.front_y = same.rear_y; same.front_z = same.rear_z;
        const tha::Aim z = tha::decide(same, lim());
        check(!z.use, "hands at exactly the same point: refuses, no divide by zero");
        check(!std::isnan(z.yaw_deg) && !std::isnan(z.pitch_deg), "coincident hands: no NaN escapes");
    }

    // ---- 4. GUARD 1, both edges, so the threshold is a real boundary and not decoration.
    {
        tha::Hands just_under = along(1, 0, 0);
        just_under.front_x = just_under.rear_x + tha::kMinSeparation - 0.001;
        just_under.front_y = just_under.rear_y;
        just_under.front_z = just_under.rear_z;
        check(!tha::decide(just_under, lim()).use, "separation: refuses just under the minimum");

        tha::Hands just_over = along(1, 0, 0);
        just_over.front_x = just_over.rear_x + tha::kMinSeparation + 0.001;
        just_over.front_y = just_over.rear_y;
        just_over.front_z = just_over.rear_z;
        check(tha::decide(just_over, lim()).use, "separation: accepts just over the minimum");
    }

    // ---- 5. GUARD 2: the off hand is not on the gun. THE CASE THIS EXISTS FOR -- the off hand is
    // holding the lantern, or resting at the player's side, while the rifle points somewhere else.
    // Aiming down the hand-to-hand line then fires at the lantern.
    {
        tha::Hands h = along(1, 0, 0);       // hands run due east, comfortably far apart
        h.fwd_x = 0.0; h.fwd_y = 1.0; h.fwd_z = 0.0;   // but the gun points due north: 90 degrees out
        const tha::Aim a = tha::decide(h, lim());
        check(!a.use, "off hand elsewhere: refuses to aim down the hand line");
        near_deg(a.disagree_deg, 90.0, "off hand elsewhere: the disagreement is reported for the log");

        // The extreme: hands crossed, the front hand BEHIND the rear one. Aiming down that line
        // would shoot the player backwards.
        tha::Hands back = along(1, 0, 0);
        back.fwd_x = -1.0; back.fwd_y = 0.0; back.fwd_z = 0.0;
        const tha::Aim b = tha::decide(back, lim());
        check(!b.use, "hands reversed: refuses rather than firing backwards");
        near_deg(b.disagree_deg, 180.0, "hands reversed: reported as fully opposed");
    }

    // ---- 6. GUARD 2, both edges.
    {
        const double a_in  = tha::kMaxDisagreeDeg - 0.5;
        const double a_out = tha::kMaxDisagreeDeg + 0.5;
        const double r = 3.14159265358979323846 / 180.0;

        tha::Hands in = along(1, 0, 0);
        in.fwd_x = std::cos(a_in * r); in.fwd_y = std::sin(a_in * r); in.fwd_z = 0.0;
        check(tha::decide(in, lim()).use, "agreement: accepts just inside the limit");

        tha::Hands out = along(1, 0, 0);
        out.fwd_x = std::cos(a_out * r); out.fwd_y = std::sin(a_out * r); out.fwd_z = 0.0;
        check(!tha::decide(out, lim()).use, "agreement: refuses just outside the limit");
    }

    // ---- 7. A non-unit weapon forward must not change the verdict. The engine hands us a unit
    // vector today, but a future caller might not, and a silently scaled dot product would move
    // the guard without anyone noticing.
    {
        tha::Hands h = along(1, 0, 0);
        h.fwd_x = 7.5; h.fwd_y = 0.0; h.fwd_z = 0.0;   // same direction, seven and a half times long
        const tha::Aim a = tha::decide(h, lim());
        check(a.use, "non-unit forward: still accepted");
        near_deg(a.disagree_deg, 0.0, "non-unit forward: still reads as no disagreement");

        // ⚠️ The case above is NOT enough on its own, and finding that out is why it is written
        // down here: with a forward pointing the SAME way, an unnormalised dot product is too big,
        // gets clamped to 1, and reads as perfect agreement -- so dropping the normalisation
        // passes. A SHORT forward at a real angle is what bites: 0.5 long at 50 degrees is inside
        // the 55-degree limit, but without normalising, the dot is 0.5*cos(50) = 0.32, which reads
        // as 71 degrees and would refuse a perfectly good two-handed hold.
        const double r = 3.14159265358979323846 / 180.0;
        tha::Hands shortf = along(1, 0, 0);
        shortf.fwd_x = 0.5 * std::cos(50.0 * r);
        shortf.fwd_y = 0.5 * std::sin(50.0 * r);
        shortf.fwd_z = 0.0;
        const tha::Aim s = tha::decide(shortf, lim());
        check(s.use, "short non-unit forward at 50 deg: accepted (length must not move the guard)");
        near_deg(s.disagree_deg, 50.0, "short non-unit forward: the angle is read as 50, not 71", 1e-6);

        tha::Hands zero = along(1, 0, 0);
        zero.fwd_x = zero.fwd_y = zero.fwd_z = 0.0;
        check(!tha::decide(zero, lim()).use, "zero-length forward: refuses rather than dividing by zero");
    }

    // ---- 8. Translation invariance. Only the difference between the hands can matter, so the same
    // hold anywhere on the map must give the same aim. If this ever fails, an absolute position has
    // crept into the maths.
    {
        tha::Hands a = along(1, 2, 0.5);
        tha::Hands b = a;
        b.rear_x += 5000.0; b.front_x += 5000.0;
        b.rear_y -= 777.0;  b.front_y -= 777.0;
        b.rear_z += 123.0;  b.front_z += 123.0;
        const tha::Aim ra = tha::decide(a, lim());
        const tha::Aim rb = tha::decide(b, lim());
        check(ra.use && rb.use, "moved across the map: both accepted");
        near_deg(ra.yaw_deg, rb.yaw_deg, "moved across the map: same yaw");
        near_deg(ra.pitch_deg, rb.pitch_deg, "moved across the map: same pitch");
    }

    // ---- 9. Scale invariance of the DIRECTION. Holding the same line with the hands further
    // apart must not change where it points -- only whether guard 1 lets it through.
    {
        tha::Hands near_h = along(2, 1, 0.3);
        tha::Hands far_h = near_h;
        const double sx = far_h.front_x - far_h.rear_x;
        const double sy = far_h.front_y - far_h.rear_y;
        const double sz = far_h.front_z - far_h.rear_z;
        far_h.front_x = far_h.rear_x + sx * 3.0;
        far_h.front_y = far_h.rear_y + sy * 3.0;
        far_h.front_z = far_h.rear_z + sz * 3.0;
        near_deg(tha::decide(near_h, lim()).yaw_deg, tha::decide(far_h, lim()).yaw_deg,
                 "hands further apart: same yaw");
        near_deg(tha::decide(near_h, lim()).pitch_deg, tha::decide(far_h, lim()).pitch_deg,
                 "hands further apart: same pitch");
    }

    std::printf("%s  (%d checks, %d failed)\n", g_fail == 0 ? "PASS" : "FAIL", g_checks, g_fail);
    return g_fail == 0 ? 0 : 1;
}
