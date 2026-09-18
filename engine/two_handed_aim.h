// two_handed_aim.h -- where does a two-handed long gun actually point? (2026-09-18, /pd)
//
// Pure maths, plain doubles, no GZDoom and no OpenVR types, so engine/two_handed_aim_test.cpp can
// compile and run THIS FILE on a machine with no engine source and no headset. The engine change
// calls it and does nothing else, so what the test checks is what ships.
//
// THE PROBLEM. Our GZDoomVR patch already tells mods where both hands are every tic
// (OffhandValid / OffhandPos / OffhandDir, and the weapon hand's AttackPos / AttackAngle /
// AttackPitch). A mod can therefore already DRAW a rifle along the line between the hands. What it
// cannot do is make the SHOT follow that line: aiming still comes from the weapon controller's own
// rotation, so the bullet leaves along wherever the rear hand happens to be tilted rather than
// along the barrel the player is looking down. The gun looks two-handed and shoots one-handed.
//
// THE FIX, in one sentence: when a mod asks for it, aim from the rear hand THROUGH the front hand.
//
// ⚠️ TWO GUARDS, AND THEY ARE THE WHOLE DESIGN. A line between two tracked points is a terrible
// aim vector exactly when the player is not actually holding a rifle with both hands, and that is
// most of the time -- hands down by the sides, off hand on a ladder, off hand holding the lantern.
// Without guards the gun would swing wildly and fire backwards, which in a headset reads as "the
// mod is broken" rather than "the off hand was not on the gun".
//
//   1. MINIMUM SEPARATION. Two nearly coincident points give a direction that is pure tracking
//      noise. Below `min_sep` we refuse.
//   2. AGREEMENT WITH THE GUN. The rear hand still says where the gun is pointed. If the hand-to-
//      hand line disagrees with that by more than `max_disagree_deg`, the front hand is not on the
//      fore-end and we refuse. This one is unit-free, which is why it carries most of the weight:
//      it works whatever the map scale turns out to be.
//
// Refusing means "leave the aim exactly as it is today", so the worst case is the behaviour we
// already have, never a wrong shot.
//
// ⚠️ WHAT IS NOT ESTABLISHED. Nothing here has been run in the game or worn. The coordinate
// convention below is read from the off-hand block of our own patch
// (`OffhandPos = DVector3(m[3][0], m[3][2], m[3][1])`, `pitch = -asin(dir.Z)`) and is therefore
// `[inferred-static 2026-09-18]`: both hand positions arrive in the same GZDoom space through the
// same conversion, so subtracting them is meaningful. If that turns out to be wrong the symptom is
// unmistakable -- the gun points somewhere consistent but wrong, rather than jittering -- and it
// is a conversion bug, not a maths bug. The sensible default for `min_sep` in map units is a guess
// until someone measures a comfortable rifle hold in the headset. [hypothesis]
#pragma once
#include <cmath>

namespace tha {

struct Hands {
    // Both in GZDoom world space (X east, Y north, Z up), as the off-hand block already produces.
    double rear_x, rear_y, rear_z;    // AttackPos: the trigger hand
    double front_x, front_y, front_z; // OffhandPos: the hand on the fore-end
    // The weapon hand's own forward direction, unit length, same space. This is what aiming uses
    // today, and it is the reference the agreement guard is measured against.
    double fwd_x, fwd_y, fwd_z;
};

struct Limits {
    double min_sep;            // map units; below this the two points are noise
    double max_disagree_deg;   // how far the hand line may differ from where the gun points
};

struct Aim {
    bool   use;         // false = leave the aim exactly as it is today
    double yaw_deg;     // GZDoom angle
    double pitch_deg;   // GZDoom pitch: POSITIVE IS DOWN, matching -asin(dir.Z) in our patch
    double sep;         // how far apart the hands were, for the log
    double disagree_deg;// how far the hand line was from the gun's own direction, for the log
};

inline double clampd(double v, double lo, double hi) { return v < lo ? lo : (v > hi ? hi : v); }

inline Aim decide(const Hands& h, const Limits& lim) {
    Aim a{};
    a.use = false;

    const double dx = h.front_x - h.rear_x;
    const double dy = h.front_y - h.rear_y;
    const double dz = h.front_z - h.rear_z;
    const double sep = std::sqrt(dx * dx + dy * dy + dz * dz);
    a.sep = sep;

    // Guard 1. Also catches the exactly-coincident case, where the normalisation below would be a
    // division by zero -- so the order of these two tests is not cosmetic.
    if (!(sep > 0.0) || sep < lim.min_sep) return a;

    const double ux = dx / sep, uy = dy / sep, uz = dz / sep;

    // Guard 2. The weapon forward is taken as unit; if the caller hands us something else the dot
    // product is still monotonic in the angle, but the reported number would be wrong, so
    // normalise defensively rather than trusting it.
    const double fl = std::sqrt(h.fwd_x * h.fwd_x + h.fwd_y * h.fwd_y + h.fwd_z * h.fwd_z);
    if (!(fl > 0.0)) return a;
    const double dot = clampd((ux * h.fwd_x + uy * h.fwd_y + uz * h.fwd_z) / fl, -1.0, 1.0);
    a.disagree_deg = std::acos(dot) * 180.0 / 3.14159265358979323846;
    if (a.disagree_deg > lim.max_disagree_deg) return a;

    // The same two formulas the off-hand block already uses, so the two-hand line is expressed in
    // exactly the convention the rest of the patch speaks.
    a.yaw_deg   = std::atan2(uy, ux) * 180.0 / 3.14159265358979323846;
    a.pitch_deg = -std::asin(clampd(uz, -1.0, 1.0)) * 180.0 / 3.14159265358979323846;
    a.use = true;
    return a;
}

// The defaults the engine change ships with. Both are guesses that the first headset session
// should replace with measurements; they are named here so that replacing them is one edit.
inline constexpr double kMinSeparation    = 8.0;   // map units. ~20 cm at the usual VR scale. UNMEASURED.
inline constexpr double kMaxDisagreeDeg   = 55.0;  // beyond this the off hand is not on the gun. UNMEASURED.

} // namespace tha
