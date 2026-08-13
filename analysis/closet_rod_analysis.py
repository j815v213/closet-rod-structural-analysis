"""
Closet Rod Structural Analysis
Jackson Vaughn

Purpose:
    Analyze a solid circular teakwood closet rod under a uniformly distributed
    clothing load using elementary beam theory.

Units:
    Length: inches
    Force: lbf
    Stress: psi
"""

import math

# 1. INPUTS
# Geometry
L_total = 62.0                 # total rod length [in]
bearing_contact = 0.75         # effective support contact per side [in]
d = 1.25                       # rod diameter [in]

# Effective span
L_e = L_total - 2 * bearing_contact

# Loading
W = 71.75                      # total estimated clothing load [lbf]
w = W / L_e                    # uniformly distributed load [lbf/in]

# Teakwood material properties
E = 1.781e6                    # elastic modulus [psi]
MOR = 14080                    # modulus of rupture [psi]
nu = 0.325                     # assumed Poisson's ratio, used in FEA only

# Serviceability / creep assumptions
deflection_limit_ratio = 240
creep_multiplier = 1.5

# SolidWorks FEA results
fea_deflection = 1.108         # max vertical displacement [in]
fea_stress = 2847              # representative midspan axial stress [psi]
fea_reaction_A = 35.875        # vertical reaction at support A [lbf]
fea_reaction_B = 35.875        # vertical reaction at support B [lbf]

# 2. SECTION PROPERTIES
I = math.pi * d**4 / 64        # area moment of inertia [in^4]
c = d / 2                      # outer fiber distance [in]

# 3. SIMPLY SUPPORTED BEAM MODEL
R_A = R_B = W / 2               # Support reactions [lbf]
x_Mmax = L_e / 2
M_max = W * L_e / 8             # Maximum bending moment [lbf*in]

# Bending stress and factor of safety
sigma_max = M_max * c / I
FS_MOR = MOR / sigma_max
delta_max = (5 * w * L_e**4) / (384 * E * I)   # Maximum vertical deflection [in]

# Serviceability check
delta_allow = L_e / deflection_limit_ratio
delta_ratio = delta_max / delta_allow
delta_creep = creep_multiplier * delta_max  # Simplified long-term creep estimate [in]

# Load capacity estimates
W_rupture = (8 * MOR * I) / (c * L_e)
W_L240 = W * (delta_allow / delta_max)

# 4. FIXED-FIXED IDEAL COMPARISON BOUND
M_fixed = W * L_e / 12
sigma_fixed = M_fixed * c/ I
delta_fixed = (w * L_e**4) / (384 * E * I)
FS_fixed = MOR / sigma_fixed

# 5. CENTER SUPPORT ESTIMATE
L_center = L_e / 2
W_center = W / 2
w_center = W_center / L_center

M_center = W_center * L_center / 8
sigma_center = M_center * c / I
delta_center = (5 * w_center * L_center**4) / (384 * E * I)
FS_center = MOR / sigma_center

# 6. SOLIDWORKS FEA COMPARISON
fea_FS = MOR / fea_stress
fea_total_reaction = fea_reaction_A + fea_reaction_B
reaction_error = fea_total_reaction - W

# 7. OUTPUT
def section(title):
    print(f"\n{title}")
    print("-" * len(title))

def line(label, value="", unit="", decimals=3):
    if isinstance(value, float):
        text = f"{value:.{decimals}f}"
    else:
        text = str(value)
    print(f"{label:<35} {text:>12} {unit}")

print("\nCLOSET ROD STRUCTURAL ANALYSIS")
print("=" * 36)

section("INPUTS")
line("Total rod length:", L_total, "in")
line("Effective support contact:", bearing_contact, "in per side")
line("Effective span:", L_e, "in")
line("Rod diameter:", d, "in")
line("Total clothing load:", W, "lbf")
line("Distributed load:", w, "lbf/in")
line("Elastic modulus, E:", f"{E:.3e}", "psi")
line("Modulus of rupture, MOR:", MOR, "psi", decimals=0)

section("SECTION PROPERTIES")
line("Moment of inertia, I:", I, "in^4", decimals=4)

section("SIMPLY SUPPORTED BEAM RESULTS")
line("Reaction at each support:", R_A, "lbf")
line("Max moment location:", x_Mmax, "in")
line("Maximum bending moment:", M_max, "lbf-in", decimals=2)
line("Maximum bending stress:", sigma_max / 1000, "ksi")
line("Factor of safety vs MOR:", FS_MOR, decimals=2)
line("Maximum vertical deflection:", delta_max, "in")
line(f"L/{deflection_limit_ratio} deflection limit:", delta_allow, "in")
line("Deflection / allowable:", delta_ratio, decimals=2)
line("Long-term deflection estimate:", delta_creep, "in")

section("LOAD CAPACITY ESTIMATES")
line("Estimated bending rupture load:", W_rupture, "lbf", decimals=1)
line(f"Load at L/{deflection_limit_ratio} deflection:", W_L240, "lbf", decimals=1)



section("SOLIDWORKS FEA COMPARISON")
line("FEA vertical deflection:", fea_deflection, "in")
line("FEA midspan axial stress:", fea_stress / 1000, "ksi")
line("FEA factor of safety vs MOR:", fea_FS, decimals=2)
line("FEA reaction at A:", fea_reaction_A, "lbf")
line("FEA reaction at B:", fea_reaction_B, "lbf")
line("FEA total vertical reaction:", fea_total_reaction, "lbf")
line("Reaction error vs load:", reaction_error, "lbf")

section("INTERPRETATION")
if FS_MOR > 1:
    print("Strength: bending rupture is not predicted under the estimated load.")
else:
    print("Strength: bending rupture is predicted under the estimated load.")

if delta_max > delta_allow:
    print(f"Serviceability: deflection exceeds the selected L/{deflection_limit_ratio} limit.")
else:
    print(f"Serviceability: deflection is below the selected L/{deflection_limit_ratio} limit.")

print("Overall: the rod is strength-acceptable, but deflection/serviceability controls.")
