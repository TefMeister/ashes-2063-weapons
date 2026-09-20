# Shotgun numbers shared by the model, shoot and reload files.
# +Y is the muzzle, +Z up, +X the gun's right side. Origin: rear face of the receiver,
# on the receiver's bottom line, so the stock runs into -Y and the barrel into +Y.
MODEL = r"C:\Users\TD3KX\github-backups\ashes-2063-weapons\shotgun\Ashes_2063_EP1_shotgun_model.blend"
REST_LOC = (0.130, 0.700, -0.170)     # where the gun sits in the first-person view
REST_ROT = (2, 18, 12)                 # pitch, cant, yaw (degrees); +yaw swings the muzzle
                                      # toward the middle of the screen

# âš ï¸ The first-person camera is 18 mm, not the kit's 32 mm default. GZDoom plays at about a
# 90-degree horizontal view; at 32 mm (about 61) the butt of a gun this long falls outside the
# Blender frame while the GAME still draws it, filling half the screen. 18 mm is the game's own
# angle, so what these files show is what the game shows [verified-live 2026-09-19, n=1 launch].
VIEW_LENS_SG = 18

BORE_Z = 0.058                        # height of the barrel's centre line
BLOCK_SG = 0.0045                     # texture pixel size: big gun, big pixels

# ---- receiver --------------------------------------------------------------
REC_LEN, REC_W, REC_H = 0.200, 0.050, 0.072
REC_Z = BORE_Z - 0.026                # receiver centre height

# ---- barrel and magazine tube ---------------------------------------------
BARREL_Y = (0.195, 0.600)             # breech end, muzzle end
BARREL_R = 0.0115
BORE_R = 0.0085
MAG_Z = BORE_Z - 0.0235               # magazine tube centre height
MAG_R = 0.0100
MAG_END_Y = 0.498                     # where the tube stops (cap sits here)
BAND_Y = 0.452                        # barrel band holding tube to barrel
SIGHT_Y = 0.578                       # front sight post

# ---- pump (forend) ---------------------------------------------------------
PUMP_Y = (0.240, 0.412)               # rest position, front to back
PUMP_PIVOT = (0.0, 0.3260, MAG_Z)
PUMP_BACK = -0.070                    # how far it racks back along -Y
RIB_COUNT, RIB_PITCH = 8, 0.0200      # the deep grooves in the wood

# ---- stock -----------------------------------------------------------------
BUTT_Y = -0.300                       # rear face of the recoil pad

# ---- shells ----------------------------------------------------------------
SHELL_R, SHELL_L = 0.0092, 0.0640     # 12-gauge hull
SHELL_BRASS_L = 0.0180                # brass head length
PORT_Y = 0.145                        # centre of the ejection port
