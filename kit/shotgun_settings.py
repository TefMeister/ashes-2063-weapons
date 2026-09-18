# Shotgun numbers shared by the model, shoot and reload files.
# +Y is the muzzle, +Z up, +X the gun's right side. Origin: rear face of the receiver,
# on the receiver's bottom line, so the stock runs into -Y and the barrel into +Y.
MODEL = r"C:\Users\TD3KX\ashes-2063-weapons\shotgun\Ashes_2063_EP1_shotgun_model.blend"
REST_LOC = (0.010, 0.10, -0.085)      # where the gun sits in the first-person view
REST_ROT = (3, -4, 6)                 # pitch, cant, yaw (degrees)

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
