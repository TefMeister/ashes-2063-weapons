"""Moving parts for the 2026-11-27 Meshy set, read from the game's own weapon states, for all three episodes (Build PC).

The sharp guns' jobs (make_job_<gun>.py) name every sprite letter by hand, for Episode 1 only. Afterglow and Hard
Reset have their own weapon files and guns Episode 1 never had, so here a weapon's states are read in order and each
frame the hand shows gets its pose from what the state it sits in DOES:
- a FIRE state (its label says fire / shoot / attack / hold): the frames drawn BRIGHT are the shot: the gun kicks,
  the trigger is back, the recoiling parts (slide, bolt) are back, flash 1, 2, 3 on the first, second, third bright
  frame; the frames after the last bright one settle (kick dies away, the slide comes home);
- a CYCLE state (pump / lever / cock / rack / chamber / bolt / slide / cycle): the cycling parts go back and come home
  over the state's frames (a triangle), hinged ones (a lever) turn out and back the same way;
- a RELOAD state (reload / load / insert / mag / clip / shell, not ready / select): magazines drop out over the first
  third, are gone in the middle and come up in the last third; break actions and swing-out cylinders open over the
  first fifth, stay open and close over the last fifth; loose rounds rise into the gun over each state whose label
  says loop / insert / shell;
- anything else (ready, select, idle): the rest pose.
Every frame is one game tic, so the timing is the game's own. A (sprite, letter) shown in several states takes the
first state it is met in, ready states first, so a ready frame stays still.

Poses are in the blend's axes, metres (sharp_job.bl turns forge axes); a hinge is [dx, dy, dz, degrees, hx, hy, hz,
axis] with axis 0 left-right, 1 along the barrel, 2 up (gz_forge_export.md3_corners).
"""
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "brutal-doom-3d-guns", "tools"))
from weapon_sprites import STATE, actor_text, hand_frames  # noqa: E402

from sharp_job import CUBE_M, bl  # noqa: E402

GAME = os.path.join("C:" + os.sep, "NonSteam", "Ashes 2063 VR", "Resources")
EPISODES = {"ep1": "Ashes2063Enriched2_23.pk3", "afterglow": "AshesAfterglow1_16.pk3", "hardreset": "AshesHardReset_105.pk3"}
# borrowed by Ashes weapons from elsewhere (forge_jobs.ASHES_FOREIGN): never a gun's own frames
FOREIGN = {"KNIF", "CHGG", "SHTG", "NULL", "GLOK", "INGG"}

FIRE_WORDS = ("fire", "shoot", "attack", "hold", "flame", "burn", "throw", "swing", "strike", "hit", "gas")
CYCLE_WORDS = ("pump", "lever", "cock", "rack", "chamber", "cycle", "bolt", "slide", "rechamber")
RELOAD_WORDS = ("reload", "load", "insert", "mag", "clip", "shell", "work", "refill")
REST_WORDS = ("ready", "select", "deselect", "spawn", "idle", "lower", "raise", "empty", "nope")
LOOP_WORDS = ("loop", "insert", "shell", "round")
LABEL = re.compile(r"^\s*([A-Za-z0-9_.]+)\s*:(?!:)")

KICK_SHOT = (0.012, 2.5)
KICK_AFTER = [(0.006, 1.2), (0.003, 0.5)]


def source(ep, wfile):
    return zipfile.ZipFile(os.path.join(GAME, EPISODES[ep])).read("Actors/Weapons/" + wfile).decode("latin-1")


def states(src, cls):
    """[(label, [(sprite, letter, tics, bright, after)]), ...] in file order; `after` is the text of the zero-tic
    action lines that follow a frame (where Ashes puts its A_FireBullets)."""
    t = actor_text(src, cls)
    if t is None:
        return []
    t = t[t.lower().find("states"):]
    out, cur, last = [], None, None
    for line in t.splitlines():
        m = STATE.match(line)
        if not m:
            lm = LABEL.match(line)
            if lm and lm.group(1).lower() not in ("goto", "loop", "stop", "wait", "fail", "states"):
                cur = (lm.group(1), [])
                out.append(cur)
            continue
        if cur is None:
            continue
        spr, letters = m.group(1), m.group(2)
        tics = re.search(r"\s(-?\d+)", line[m.start(2) + len(letters):])
        tics = int(tics.group(1)) if tics else 1
        bright = " bright" in line.lower()
        if spr in ("TNT1", "####", "----") or tics == 0:
            if last is not None:
                last[4] += line + "\n"
            continue
        for L in letters:
            f = [spr, L, tics, bright, ""]
            cur[1].append(f)
            last = f
    return out


def kind(label, frames):
    n = label.lower()
    if any(w in n for w in REST_WORDS) and not any(w in n for w in ("reload",)):
        return "rest"
    if any(w in n for w in CYCLE_WORDS):
        return "cycle"
    if any(w in n for w in RELOAD_WORDS):
        return "reload"
    if any(w in n for w in FIRE_WORDS):
        return "fire"
    return "rest"


def frame_contexts(src, cls, foreign=FOREIGN):
    """{(sprite, letter): (kind, label, index, count, shot_rank or None, after_shot or None)} for every frame the hand
    shows. shot_rank: 0, 1, 2 ... for the bright frames of a fire state; after_shot: 0, 1 ... for the frames after."""
    shown = set(hand_frames(src, cls, foreign))
    def rank_of(s):
        """Named rest states first (a ready frame stays still), then the doing states, then unnamed ones."""
        n = s[0].lower()
        if kind(*s) == "rest":
            return 0 if any(w in n for w in REST_WORDS) else 2
        return 1
    order = sorted(states(src, cls), key=rank_of)
    ctx = {}
    for label, frames in order:
        k = kind(label, frames)
        n = len(frames)
        bright = [i for i, f in enumerate(frames) if f[3]]
        if k == "fire" and not bright:
            fired = [i for i, f in enumerate(frames) if re.search(r"(?i)A_Fire|A_RailAttack|A_CustomPunch|"
                                                                    r"A_CustomBulletAttack|A_GunFlash", f[4])]
            bright = fired[:1] or [0]
        for i, f in enumerate(frames):
            key = (f[0], f[1])
            if key not in shown or key in ctx:
                continue
            rank = bright.index(i) if k == "fire" and i in bright else None
            after = (i - bright[-1] - 1) if k == "fire" and bright and i > bright[-1] else None
            ctx[key] = (k, label, i, n, rank, after)
    for key in shown:
        ctx.setdefault(key, ("rest", "", 0, 1, None, None))
    return ctx


def triangle(i, n):
    """0 -> 1 -> 0 over a state's frames (peak in the middle)."""
    if n <= 1:
        return 1.0
    s = i / (n - 1)
    return 1.0 - abs(2.0 * s - 1.0)


def open_share(i, n, edge=0.2):
    if n <= 2:
        return 1.0
    s = i / (n - 1)
    return min(1.0, s / edge, (1.0 - s) / edge) if edge else 1.0


class Rig:
    """What a gun's parts do. All lengths in main cubes (forge axes) unless said; hinges in forge main cubes too.
    recoil: {part: cubes back along -x on a shot}; forward: {part: cubes forward on a shot} (the ram's head);
    cycle: {part: cubes back over a cycle state}; cycle_hinge: {part: (degrees, (hx, hy, hz), axis)};
    trigger: part name; trigger_back: cubes; flashes: [names] (sharp_kit.flashes, parked park_z(k) above);
    mags: {part: cubes down when out}; open_hinge: {part: (degrees, (hx, hy, hz), axis)} for reload states;
    rounds: {part: (dx, dy, dz) cubes it starts from, rising to its built spot over a loop state};
    cycle_in_reload: the cycling parts also cycle once in a reload state (a pump racked before loading)."""

    def __init__(self, **kw):
        self.recoil = kw.get("recoil", {})
        self.forward = kw.get("forward", {})
        self.cycle = kw.get("cycle", {})
        self.cycle_hinge = kw.get("cycle_hinge", {})
        self.trigger = kw.get("trigger", "trigger")
        self.trigger_back = kw.get("trigger_back", 1.5)
        self.flashes = kw.get("flashes", ["flash_a", "flash_b", "flash_c"])
        self.mags = kw.get("mags", {})
        self.open_hinge = kw.get("open_hinge", {})
        self.rounds = kw.get("rounds", {})
        self.cycle_in_reload = kw.get("cycle_in_reload", False)
        # spent: {part: (dx, dy, dz) cubes}: a part the shot uses up (the crossbow's bolt): gone from the shot to the
        # end of the fire state, slid in from that offset over a reload state, in place otherwise
        self.spent = kw.get("spent", {})
        self.kick = kw.get("kick", 1.0)
        self.fire_recoil_frames = kw.get("fire_recoil_frames", 2)

    def parts(self):
        return (list(self.recoil) + list(self.forward) + list(self.cycle) + list(self.cycle_hinge)
                + ([self.trigger] if self.trigger else []) + list(self.flashes) + list(self.mags)
                + list(self.open_hinge) + list(self.rounds) + list(self.spent))

    def hidden(self):
        return list(self.flashes) + list(self.mags) + list(self.rounds) + list(self.spent)


def _hinge(deg, h, axis, share):
    hx, hy, hz = bl(*(c * CUBE_M for c in h))
    return [0.0, 0.0, 0.0, deg * share, hx, hy, hz, axis]


def pose_fn(rig, ctx, park_z):
    """pose(spr, L) -> {part: pose} and kick(spr, L) -> (m, deg) for build_job."""
    def pose(spr, L):
        k, label, i, n, rank, after = ctx[(spr, L)]
        p = {}
        for part in list(rig.mags) + list(rig.spent):
            p[part] = [0.0, 0.0, 0.0]
        if k == "fire" and (rank is not None or after is not None):
            for part in rig.spent:
                p.pop(part, None)
        if k == "reload":
            s = i / max(1, n - 1)
            for part, (dx, dy, dz) in rig.spent.items():
                t = 1.0 - s
                p[part] = bl(dx * t * CUBE_M, dy * t * CUBE_M, dz * t * CUBE_M)
        if k == "fire":
            if rank is not None:
                if rank < len(rig.flashes):
                    p[rig.flashes[rank]] = bl(0.0, 0.0, -park_z(rank) * CUBE_M)
                if rig.trigger:
                    p[rig.trigger] = bl(-rig.trigger_back * CUBE_M, 0.0, 0.0)
                for part, d in rig.recoil.items():
                    p[part] = bl(-d * CUBE_M, 0.0, 0.0)
                for part, d in rig.forward.items():
                    p[part] = bl(d * CUBE_M, 0.0, 0.0)
            elif after is not None and after < rig.fire_recoil_frames:
                share = 1.0 - (after + 1) / (rig.fire_recoil_frames + 1)
                for part, d in rig.recoil.items():
                    p[part] = bl(-d * share * CUBE_M, 0.0, 0.0)
                for part, d in rig.forward.items():
                    p[part] = bl(d * share * CUBE_M, 0.0, 0.0)
        elif k == "cycle" or (k == "reload" and rig.cycle_in_reload and not any(w in label.lower()
                                                                                 for w in LOOP_WORDS)):
            s = triangle(i, n)
            for part, d in rig.cycle.items():
                p[part] = bl(-d * s * CUBE_M, 0.0, 0.0)
            for part, (deg, h, axis) in rig.cycle_hinge.items():
                p[part] = _hinge(deg, h, axis, s)
        if k == "reload":
            s = i / max(1, n - 1)
            loop = any(w in label.lower() for w in LOOP_WORDS)
            for part, d in rig.mags.items():
                if loop:
                    continue
                if s < 1 / 3:
                    p[part] = bl(0.0, 0.0, -d * (s * 3) * CUBE_M)
                elif s > 2 / 3:
                    p[part] = bl(0.0, 0.0, -d * ((1 - s) * 3) * CUBE_M)
                else:
                    p.pop(part, None)                     # out of the gun: not drawn
            share = 1.0 if loop else open_share(i, n)
            for part, (deg, h, axis) in rig.open_hinge.items():
                p[part] = _hinge(deg, h, axis, share)
            if loop:
                for part, (dx, dy, dz) in rig.rounds.items():
                    t = 1.0 - s
                    p[part] = bl(dx * t * CUBE_M, dy * t * CUBE_M, dz * t * CUBE_M)
        return {a: b for a, b in p.items()}

    def kick(spr, L):
        k, label, i, n, rank, after = ctx[(spr, L)]
        if k != "fire":
            return (0.0, 0.0)
        if rank is not None:
            return (KICK_SHOT[0] * rig.kick, KICK_SHOT[1] * rig.kick)
        if after is not None and after < len(KICK_AFTER):
            return (KICK_AFTER[after][0] * rig.kick, KICK_AFTER[after][1] * rig.kick)
        return (0.0, 0.0)
    return pose, kick


def report(ep, wfile, cls):
    """What each frame was read as (for checking a gun by eye)."""
    ctx = frame_contexts(source(ep, wfile), cls)
    for key in sorted(ctx):
        print(" ".join(key), *ctx[key])
