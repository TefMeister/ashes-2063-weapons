"""Build the player release of the Ashes 2063 3D weapons for VR, as one zip.

    python tools/make_release.py 0.1.0

What goes in is decided by Tefa (2026-09-23): the revolver as it is (no hands), the cube pistol with
its half-glove hand, the cube lantern held by its handle, and the shotgun with gloved hands and the
two-handed grip. The free LEFT HAND is left out on purpose - it is still wrong.

Nothing is rebuilt from Blender here. Every game file is the one Tefa last wore, copied as it is; the
only change is that the loose left hand is cut out of the lantern file, so the lantern itself stays
byte-for-byte what was approved. Every file's SHA-256 goes into MANIFEST.txt, and the zip is kept.
"""
import datetime, hashlib, os, re, shutil, subprocess, sys, zipfile
from pathlib import Path

# ---- settings: where today's approved files live (home PC) -------------------------------------
HOME = Path(os.path.expanduser("~"))
REPO = Path(__file__).resolve().parent.parent
PICS = HOME / "Pictures" / "Screenshots"
GAME = Path("C:/NonSteam/Ashes 2063 VR")
ENGINE_SRC = GAME / "gzdoomvr-tefa"                       # our GZDoomVR build, the one worn
ENGINE_GIT = HOME / "gzdoomvr-src" / "gzdoomvr"           # its source: upstream tag + our commits
UPSTREAM_TAG = "gvr4.13.2.2"
UPSTREAM_URL = "https://github.com/hh79/gzdoomvr"

PK3S = [  # (file name in the release, source) - load order is the order tested in the headset
    ("1_revolver.pk3", REPO / "revolver" / "gzdoom" / "Ashes2063_revolver3d_VR_test.pk3"),
    ("2_pistol.pk3", PICS / "ashes pistol" / "blender" / "gzdoom" / "Ashes2063_voxelpistol_VR_test.pk3"),
    ("3_shotgun.pk3", REPO / "shotgun" / "gzdoom" / "Ashes2063_shotgun3d_hands_VR_test.pk3"),
    ("4_lantern.pk3", PICS / "ashes lantern" / "blender" / "gzdoom" / "Ashes2063_cube_lantern_and_hand_VR_test.pk3"),
]
LANTERN_OUT = "4_lantern.pk3"
HAND_FILES = re.compile(r"(cube_left_hand\.(md3|png)$)|(^sprites/LHND)", re.I)

# engine files that are ours to leave behind: settings, and the backups kept beside each rebuild
ENGINE_SKIP = re.compile(r"(\.ini$)|(\.pre-[\w-]+$)|(\.bak)|(\.pdb$)", re.I)

PACK = "3DWeapons"                  # the folder the release puts beside the game's Resources folder
TEMPLATES = REPO / "mod" / "release"
DIST = REPO / "dist"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ---- the lantern without the loose left hand ----------------------------------------------------
def cut_block(text, start_pat, what):
    """Remove one brace-balanced block that begins at the first match of start_pat."""
    m = re.search(start_pat, text, re.M)
    if not m:
        sys.exit(f"make_release: could not find {what} in the lantern file - the generator changed?")
    i = text.index("{", m.end() - 1)
    depth = 0
    for j in range(i, len(text)):
        depth += {"{": 1, "}": -1}.get(text[j], 0)
        if depth == 0:
            end = j + 1
            while end < len(text) and text[end] in "\r\n":
                end += 1
            return text[:m.start()] + text[end:]
    sys.exit(f"make_release: unbalanced braces around {what}")


def lantern_only(src, dst):
    zin = zipfile.ZipFile(src)
    zs = zin.read("zscript.txt").decode("utf-8")
    zs = cut_block(zs, r"^// the player's own empty left hand\nclass TefaLeftHand", "the hand's actor")
    zs = cut_block(zs, r"^\tbool IsOneHanded\(PlayerInfo p\)\n\t", "the one-handed test")
    for old, new in [
        ("// Cube lantern and bare left hand, both drawn on the off-hand controller.",
         "// Cube lantern, drawn on the off-hand controller. Release build: the bare left hand is left out\n"
         "// until it is right (Tefa, 2026-09-23)."),
        ("\tActor hand;\n", ""),
        ("\t\tbool wantHand = tracked && !lit && IsOneHanded(players[consoleplayer]);\n", ""),
    ]:
        if old not in zs:
            sys.exit(f"make_release: expected text not found in the lantern script: {old[:50]!r}")
        zs = zs.replace(old, new, 1)
    zs = cut_block(zs, r"^\t\tif \(!hand && wantHand\)\n\t\t", "the hand spawn")
    zs = cut_block(zs, r"^\t\tif \(hand\)\n\t\t", "the hand update")
    if re.search(r"TefaLeftHand|LHND|wantHand|IsOneHanded|!hand\b|\bhand\s*[.=)]", zs):
        sys.exit("make_release: something of the hand is still in the lantern script")
    md = cut_block(zin.read("modeldef.cubehands").decode("utf-8"), r"^Model TefaLeftHand\s*\n", "the hand model")
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            if HAND_FILES.search(info.filename):
                continue
            data = zin.read(info.filename)
            if info.filename == "zscript.txt":
                data = zs.encode("utf-8")
            elif info.filename == "modeldef.cubehands":
                data = md.encode("utf-8")
            zout.writestr(info.filename, data)
    kept = zipfile.ZipFile(dst).namelist()
    print(f"  lantern: {len(zin.namelist())} files in, {len(kept)} out (loose hand removed)")


# ---- the source we must publish with our engine build (GPL-3.0) ---------------------------------
def engine_source(out):
    out.mkdir(parents=True, exist_ok=True)
    g = ["git", "-C", str(ENGINE_GIT)]
    if subprocess.run(g + ["status", "--porcelain"], capture_output=True, text=True).stdout.strip():
        sys.exit("make_release: the engine source has uncommitted changes - the build would not match it")
    subprocess.run(g + ["format-patch", "-q", f"{UPSTREAM_TAG}..HEAD", "-o", str(out)], check=True)
    head = subprocess.run(g + ["rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    # the engine's own licence texts travel with the binary (GPL-3.0 and the libraries it names)
    shutil.copy2(ENGINE_GIT / "LICENSE", out.parent / "ENGINE-LICENSE.txt")
    shutil.copytree(ENGINE_GIT / "docs" / "licenses", out.parent / "engine-licenses", dirs_exist_ok=True)
    exe = ENGINE_SRC / "gzdoomvr.exe"
    newer = [p for p in (ENGINE_GIT / "src").rglob("*") if p.is_file() and p.stat().st_mtime > exe.stat().st_mtime]
    if newer:
        sys.exit(f"make_release: {len(newer)} source file(s) changed after the engine was built - rebuild first")
    (out / "HOW-TO-BUILD.txt").write_text(
        f"The engine in ../engine is GZDoomVR by hh79 ({UPSTREAM_URL}), tag {UPSTREAM_TAG}, GPL-3.0,\n"
        f"with the patches in this folder applied in number order (our commit {head}).\n\n"
        "  git clone https://github.com/hh79/gzdoomvr && cd gzdoomvr\n"
        f"  git checkout {UPSTREAM_TAG}\n  git am <this folder>/*.patch\n\n"
        "Build notes (Windows, VS 2022 + CMake), and what each change does:\n"
        "https://github.com/TefMeister/ashes-2063-weapons/tree/main/engine\n", encoding="utf-8", newline="\r\n")
    return head


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"\d+\.\d+\.\d+", sys.argv[1]):
        sys.exit("usage: python tools/make_release.py <version, e.g. 0.1.0>")
    ver = sys.argv[1]
    name = f"Ashes2063-3DWeapons-VR-v{ver}"
    stage = DIST / name
    if stage.exists():
        shutil.rmtree(stage)
    pack = stage / PACK
    for _, src in PK3S:
        if not src.is_file():
            sys.exit(f"make_release: missing {src}")

    print(f"building {name}")
    (pack / "pk3").mkdir(parents=True)
    for out, src in PK3S:
        if out == LANTERN_OUT:
            lantern_only(src, pack / "pk3" / out)
        else:
            shutil.copy2(src, pack / "pk3" / out)
    shutil.copytree(ENGINE_SRC, pack / "engine", ignore=lambda d, names: [n for n in names if ENGINE_SKIP.search(n)])
    head = engine_source(pack / "source" / "gzdoomvr-changes")
    for t in TEMPLATES.iterdir():
        dst = stage / t.name if t.suffix == ".bat" else pack / t.name
        text = t.read_text(encoding="utf-8").replace("{VERSION}", ver)
        dst.write_text(text, encoding="utf-8", newline="\r\n")

    lines = [f"{name} - built {datetime.date.today()} - engine commit {head}", ""]
    for p in sorted(stage.rglob("*")):
        if p.is_file():
            lines.append(f"{sha(p)}  {p.stat().st_size:>10}  {p.relative_to(stage).as_posix()}")
    (pack / "MANIFEST.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\r\n")

    zpath = DIST / f"{name}.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(stage.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(stage).as_posix())
    print(f"  {zpath.name}: {zpath.stat().st_size / 1e6:.1f} MB, sha256 {sha(zpath)}")


if __name__ == "__main__":
    main()
