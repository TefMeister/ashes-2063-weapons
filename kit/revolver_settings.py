# Revolver numbers shared by the model, shoot and reload files.
MODEL = r"C:\Users\TD3KX\github-backups\ashes-2063-weapons\revolver\Ashes_2063_EP1_revolver_model.blend"
REST_LOC = (-0.005, 0.24, -0.062)     # where the gun sits in the first-person view (same as the handgun)
REST_ROT = (4, -10, 20)              # pitch, cant, yaw (degrees)

BORE_Z = 0.040                       # height of the barrel's centre line
CYL_R = 0.021                        # cylinder radius
CYL_L = 0.042                        # cylinder length (front to back)
CHAMBER_R = 0.0125                   # chamber centre distance from the cylinder axis
CYL_Z = BORE_Z - CHAMBER_R           # cylinder axis height (top chamber lines up with the bore)
CRANE_PIVOT = (-0.012, 0.023, 0.006) # hinge the cylinder swings out on (left side)
CRANE_OPEN_DEG = -105                # swing-out angle (to the player's left)
CASE_R, CASE_L = 0.0048, 0.033       # .45 cartridge case
GRIP_TILT_DEG = -20                  # bottom of the grip leans back
