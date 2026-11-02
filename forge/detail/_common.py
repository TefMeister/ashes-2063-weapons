# Shared start for the DETAILED Ashes forge guns (2026-11-02): the first-pass colours from ../_common.py, plus the
# wasteland layer. Tefa, 2026-11-02: "modify the existing weapons in ashes to have a LOT of small details to them,
# make them very complex and use different qube sizes", gun only (the body rig's hands dock onto them).
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("ashes_forge_common", os.path.join(HERE, "..", "_common.py"))
_base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_base)                      # puts blender-cubekit on the path, defines the colours
globals().update({k: v for k, v in vars(_base).items() if not k.startswith("__")})
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import _wasteland as wl                              # noqa: E402,F401
