// two_handed_pose_test.cpp -- does the DRAWN gun point at the off hand?
// Build + run (MSVC):  cl /nologo /EHsc /W3 /std:c++17 two_handed_pose_test.cpp && two_handed_pose_test.exe
//            (gcc):    g++ -O2 -std=c++17 -o two_handed_pose_test two_handed_pose_test.cpp && ./two_handed_pose_test
//
// Companion to two_handed_aim_test.cpp. That one pins where the SHOT goes; this one pins which way
// the gun is DRAWN, which is the half a person can actually see -- and the half whose absence read,
// from inside the headset, as "the left hand does nothing" (2026-09-20).
//
// This compiles the SHIPPED header, not a copy of it. Ground truth is built independently: each case
// says where the hands are in plain geometry and asserts what a person would see, rather than
// re-deriving it with the formula under test.
//
// Space: OpenVR absolute tracking space. Right-handed, metres, X right, Y up, Z backwards -- so the
// direction a controller POINTS is its -Z. Getting that sign backwards is the most likely mistake
// here and it would be obvious in a headset (the gun would point behind you), but it is free to pin.
#include "two_handed_pose.h"
#include <cstdio>
#include <cmath>

static int g_fail = 0;
static int g_checks = 0;

static void check(bool cond, const char* what) {
    ++g_checks;
    if (!cond) { ++g_fail; std::printf("  FAIL: %s\n", what); }
}

static void near_num(double got, double want, const char* what, double tol = 1e-9) {
    ++g_checks;
    if (std::fabs(got - want) > tol) {
        ++g_fail;
        std::printf("  FAIL: %s (got %.12f, want %.12f)\n", what, got, want);
    }
}

static void near_vec(const double got[3], double wx, double wy, double wz, const char* what, double tol = 1e-9) {
    ++g_checks;
    if (std::fabs(got[0] - wx) > tol || std::fabs(got[1] - wy) > tol || std::fabs(got[2] - wz) > tol) {
        ++g_fail;
        std::printf("  FAIL: %s (got %.9f %.9f %.9f, want %.9f %.9f %.9f)\n",
                    what, got[0], got[1], got[2], wx, wy, wz);
    }
}

static double dot3(const double a[3], const double b[3]) {
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2];
}

// The controller sitting level and facing straight ahead: X right, Y up, Z backwards.
static thp::Basis level_hand() {
    thp::Basis b;
    b.x[0] = 1; b.x[1] = 0; b.x[2] = 0;
    b.y[0] = 0; b.y[1] = 1; b.y[2] = 0;
    b.z[0] = 0; b.z[1] = 0; b.z[2] = 1;
    return b;
}

// Every frame this produces must be a proper right-handed set of axes, or the gun renders sheared,
// mirrored, or inside out.
static void check_frame_is_sane(const thp::Basis& b, const char* what) {
    char msg[256];
    std::snprintf(msg, sizeof(msg), "%s: X is unit length", what);
    near_num(std::sqrt(dot3(b.x, b.x)), 1.0, msg, 1e-9);
    std::snprintf(msg, sizeof(msg), "%s: Y is unit length", what);
    near_num(std::sqrt(dot3(b.y, b.y)), 1.0, msg, 1e-9);
    std::snprintf(msg, sizeof(msg), "%s: Z is unit length", what);
    near_num(std::sqrt(dot3(b.z, b.z)), 1.0, msg, 1e-9);
    std::snprintf(msg, sizeof(msg), "%s: X and Y square to each other", what);
    near_num(dot3(b.x, b.y), 0.0, msg, 1e-9);
    std::snprintf(msg, sizeof(msg), "%s: Y and Z square to each other", what);
    near_num(dot3(b.y, b.z), 0.0, msg, 1e-9);
    std::snprintf(msg, sizeof(msg), "%s: Z and X square to each other", what);
    near_num(dot3(b.z, b.x), 0.0, msg, 1e-9);
    // Right-handed means X = Y x Z. A left-handed frame would mirror the gun model.
    double cx[3];
    thp::cross3(b.y, b.z, cx);
    std::snprintf(msg, sizeof(msg), "%s: right-handed (X = Y x Z)", what);
    near_vec(b.x, cx[0], cx[1], cx[2], msg, 1e-9);
}

// The whole promise of this file, stated the way Tefa stated it: the gun's line, started at the
// right hand, runs through the left hand.
static void check_points_at_front(const thp::Result& r, const double rear[3], const double front[3], const char* what) {
    const double fwd[3] = { -r.basis.z[0], -r.basis.z[1], -r.basis.z[2] };
    double want[3] = { front[0] - rear[0], front[1] - rear[1], front[2] - rear[2] };
    const double len = std::sqrt(dot3(want, want));
    want[0] /= len; want[1] /= len; want[2] /= len;
    char msg[256];
    std::snprintf(msg, sizeof(msg), "%s: the barrel points at the off hand", what);
    near_vec(fwd, want[0], want[1], want[2], msg, 1e-9);
}

int main() {
    std::printf("two-handed DRAW (where the gun points on screen)\n");

    const double origin[3] = { 0, 0, 0 };

    // 1. Off hand straight out in front: nothing should change.
    {
        const double front[3] = { 0, 0, -0.5 };
        thp::Result r = thp::aim_along_hands(level_hand(), origin, front);
        check(r.used, "straight ahead: used");
        near_num(r.gap, 0.5, "straight ahead: hands 50 cm apart");
        near_vec(r.basis.x, 1, 0, 0, "straight ahead: X unchanged");
        near_vec(r.basis.y, 0, 1, 0, "straight ahead: Y unchanged");
        near_vec(r.basis.z, 0, 0, 1, "straight ahead: Z unchanged");
        check_frame_is_sane(r.basis, "straight ahead");
        check_points_at_front(r, origin, front, "straight ahead");
    }

    // 2. Off hand out to the RIGHT: the gun swings right, and it stays level.
    {
        const double front[3] = { 0.6, 0, 0 };
        thp::Result r = thp::aim_along_hands(level_hand(), origin, front);
        check(r.used, "to the right: used");
        near_vec(r.basis.z, -1, 0, 0, "to the right: the gun's Z points left");
        near_vec(r.basis.y, 0, 1, 0, "to the right: still level (up is still up)");
        check_frame_is_sane(r.basis, "to the right");
        check_points_at_front(r, origin, front, "to the right");
    }

    // 3. Off hand out to the LEFT -- the mirror of case 2, so a swapped sign shows up here.
    {
        const double front[3] = { -0.6, 0, 0 };
        thp::Result r = thp::aim_along_hands(level_hand(), origin, front);
        check(r.used, "to the left: used");
        near_vec(r.basis.z, 1, 0, 0, "to the left: the gun's Z points right");
        near_vec(r.basis.y, 0, 1, 0, "to the left: still level");
        check_frame_is_sane(r.basis, "to the left");
        check_points_at_front(r, origin, front, "to the left");
    }

    // 4. Off hand RAISED, 45 degrees up and ahead. The gun must go up, not down. This is the same
    //    class of mistake the aim test guards: a flipped vertical reads as plausible and shoots high.
    {
        const double s = 0.7071067811865476;
        const double front[3] = { 0, s, -s };
        thp::Result r = thp::aim_along_hands(level_hand(), origin, front);
        check(r.used, "raised: used");
        check(-r.basis.z[1] > 0.5, "raised: the barrel is pointing UP, not down");
        check_frame_is_sane(r.basis, "raised");
        check_points_at_front(r, origin, front, "raised");
    }

    // 5. Off hand LOWERED.
    {
        const double s = 0.7071067811865476;
        const double front[3] = { 0, -s, -s };
        thp::Result r = thp::aim_along_hands(level_hand(), origin, front);
        check(r.used, "lowered: used");
        check(-r.basis.z[1] < -0.5, "lowered: the barrel is pointing DOWN");
        check_frame_is_sane(r.basis, "lowered");
        check_points_at_front(r, origin, front, "lowered");
    }

    // 6. Straight UP -- the awkward one, where the gun's own up axis is the direction of travel and
    //    there is no longer anything to orthogonalise against. The fallback must still give a sane
    //    frame that points the right way.
    {
        const double front[3] = { 0, 0.4, 0 };
        thp::Result r = thp::aim_along_hands(level_hand(), origin, front);
        check(r.used, "straight up: used");
        check_frame_is_sane(r.basis, "straight up");
        check_points_at_front(r, origin, front, "straight up");
    }

    // 7. Straight DOWN -- the other end of the same awkward case.
    {
        const double front[3] = { 0, -0.4, 0 };
        thp::Result r = thp::aim_along_hands(level_hand(), origin, front);
        check(r.used, "straight down: used");
        check_frame_is_sane(r.basis, "straight down");
        check_points_at_front(r, origin, front, "straight down");
    }

    // 8. HOW FAR APART THE HANDS ARE MUST NOT MATTER. Tefa asked for exactly this: how far the
    //    controllers are apart should not come into it. Near and far in the same direction must
    //    give the same gun.
    {
        const double near_front[3] = { 0.1, 0.05, -0.2 };
        const double far_front[3]  = { 0.5, 0.25, -1.0 };
        thp::Result a = thp::aim_along_hands(level_hand(), origin, near_front);
        thp::Result b = thp::aim_along_hands(level_hand(), origin, far_front);
        check(a.used && b.used, "near and far: both used");
        near_vec(a.basis.x, b.basis.x[0], b.basis.x[1], b.basis.x[2], "near and far: same X");
        near_vec(a.basis.y, b.basis.y[0], b.basis.y[1], b.basis.y[2], "near and far: same Y");
        near_vec(a.basis.z, b.basis.z[0], b.basis.z[1], b.basis.z[2], "near and far: same Z");
    }

    // 9. THE REAR HAND IS THE ANCHOR AND ITS TWIST IS KEPT. Roll the right wrist a quarter turn with
    //    the off hand straight ahead, and the gun should come out rolled by the same quarter turn.
    {
        thp::Basis rolled;                                   // rolled 90 degrees about the barrel
        rolled.x[0] = 0; rolled.x[1] = 1; rolled.x[2] = 0;   // the old up is the new right
        rolled.y[0] = -1; rolled.y[1] = 0; rolled.y[2] = 0;  // the old left is the new up
        rolled.z[0] = 0; rolled.z[1] = 0; rolled.z[2] = 1;
        const double front[3] = { 0, 0, -0.5 };
        thp::Result r = thp::aim_along_hands(rolled, origin, front);
        check(r.used, "wrist rolled: used");
        near_vec(r.basis.x, 0, 1, 0, "wrist rolled: the roll is kept (X)");
        near_vec(r.basis.y, -1, 0, 0, "wrist rolled: the roll is kept (Y)");
        near_vec(r.basis.z, 0, 0, 1, "wrist rolled: still pointing ahead");
        check_frame_is_sane(r.basis, "wrist rolled");
    }

    // 10. THE REAR HAND'S OWN AIM IS IGNORED. Point the right wrist somewhere else entirely; the gun
    //     must still follow the hands, because that is the whole point.
    {
        thp::Basis turned;                                   // controller turned 90 degrees to the right
        turned.x[0] = 0; turned.x[1] = 0; turned.x[2] = 1;
        turned.y[0] = 0; turned.y[1] = 1; turned.y[2] = 0;
        turned.z[0] = -1; turned.z[1] = 0; turned.z[2] = 0;
        const double front[3] = { 0, 0, -0.5 };
        thp::Result r = thp::aim_along_hands(turned, origin, front);
        check(r.used, "wrist turned away: used");
        check_points_at_front(r, origin, front, "wrist turned away");
        check_frame_is_sane(r.basis, "wrist turned away");
    }

    // 11. Both hands in the same place: refuse, and refusing means the gun is left exactly as the
    //     engine draws it today.
    {
        const double front[3] = { 0.005, 0, -0.005 };
        thp::Result r = thp::aim_along_hands(level_hand(), origin, front);
        check(!r.used, "hands together: refused");
        check(r.gap < thp::kMinHandGapMetres, "hands together: the gap is reported");
    }

    // 12. Just over the guard: 3 cm apart is still two-handed. The guard is a divide-by-zero
    //     safeguard only -- it is NOT a "are you really holding it?" test.
    {
        const double front[3] = { 0, 0, -0.03 };
        thp::Result r = thp::aim_along_hands(level_hand(), origin, front);
        check(r.used, "3 cm apart: still used");
    }

    // 13. The rear hand is not at the world origin -- only the line between the hands matters.
    {
        const double rear[3] = { 12.5, -3.25, 7.0 };
        const double front[3] = { 12.5, -3.25, 6.3 };   // 70 cm straight ahead of it
        thp::Result r = thp::aim_along_hands(level_hand(), rear, front);
        check(r.used, "off the origin: used");
        near_num(r.gap, 0.7, "off the origin: hands 70 cm apart", 1e-12);
        check_points_at_front(r, rear, front, "off the origin");
    }

    std::printf("%d checks, %d failures\n", g_checks, g_fail);
    return g_fail ? 1 : 0;
}
