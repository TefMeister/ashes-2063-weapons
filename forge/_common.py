# Shared start for every Ashes forge gun: finds blender-cubekit (cloned beside this repo) and the Ashes colours.
# Colours are picked from the game's own pickup and in-hand pictures (sRGB 0-255).
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "blender-cubekit")))

from forge import Model, mix, mul, hash01          # noqa: E402,F401
import forge_parts as fp                            # noqa: E402,F401

BLACK = (50, 52, 57)            # blued steel, worn black (the pictures' receivers read dark grey, not black)
STEEL = (112, 114, 120)            # bare steel
STEEL_HI = (150, 152, 156)
DARK = (14, 14, 15)
WOOD = (150, 88, 44)            # the pump's and stocks' orange-brown wood
WOOD_DK = (88, 46, 20)
WOOD_RED = (120, 62, 34)
TAPE_BLUE = (52, 84, 140)       # the blue tape on the Ashes shotgun's grip
TAPE = (40, 40, 44)
BRASS = (176, 136, 60)
RED_SHELL = (150, 30, 24)
RUST = (118, 58, 26)
GRIME = (44, 34, 24)
CUT = (12, 12, 13)              # floor of a cut
SCREW = (78, 80, 86)
COPPER = (170, 96, 52)
