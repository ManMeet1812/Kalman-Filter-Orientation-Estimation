import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

FUSION_CSV = "fus_dynamic.csv"   # change to your actual filename

def wrap_pi(a):
    while a > np.pi:  a -= 2*np.pi
    while a < -np.pi: a += 2*np.pi
    return a

def euler_to_R(roll, pitch, yaw):
    """Z-Y-X rotation (yaw-pitch-roll). Angles in radians."""
    cr, sr = np.cos(roll), np.sin(roll)
    cp, sp = np.cos(pitch), np.sin(pitch)
    cy, sy = np.cos(yaw), np.sin(yaw)

    Rz = np.array([[cy, -sy, 0],
                   [sy,  cy, 0],
                   [ 0,   0, 1]])
    Ry = np.array([[ cp, 0, sp],
                   [  0, 1,  0],
                   [-sp, 0, cp]])
    Rx = np.array([[1,  0,   0],
                   [0, cr, -sr],
                   [0, sr,  cr]])
    return Rz @ Ry @ Rx

def make_box(size=(1.4, 0.9, 0.7)):
    lx, ly, lz = size
    x, y, z = lx/2, ly/2, lz/2
    V = np.array([
        [-x,-y,-z],[ x,-y,-z],[ x, y,-z],[-x, y,-z],
        [-x,-y, z],[ x,-y, z],[ x, y, z],[-x, y, z],
    ])
    faces = [[0,1,2,3],[4,5,6,7],[0,1,5,4],[2,3,7,6],[1,2,6,5],[0,3,7,4]]
    return V, faces

# ---- Load fusion CSV robustly ----
df = pd.read_csv(FUSION_CSV, header=None)

# If first row contains text like 'time_ms' or 'roll_deg', drop it
if df.iloc[0].astype(str).str.contains("roll|pitch|yaw|time|method", case=False).any():
    df = df.iloc[1:].reset_index(drop=True)

# Keep only rows with at least 6 columns
df = df.dropna(subset=[0,1,2,3,4,5])

# Columns by your Arduino print:
# 0=time_ms, 1=FUS, 2=roll_deg, 3=pitch_deg, 4=yaw_deg, 5=compute_us
roll_deg  = pd.to_numeric(df.iloc[:, 2], errors="coerce").to_numpy()
pitch_deg = pd.to_numeric(df.iloc[:, 3], errors="coerce").to_numpy()
yaw_deg   = pd.to_numeric(df.iloc[:, 4], errors="coerce").to_numpy()

mask = np.isfinite(roll_deg) & np.isfinite(pitch_deg) & np.isfinite(yaw_deg)
roll_deg, pitch_deg, yaw_deg = roll_deg[mask], pitch_deg[mask], yaw_deg[mask]

print("Samples:", len(roll_deg))

# downsample for smooth animation
step = max(1, len(roll_deg)//600)
roll_deg, pitch_deg, yaw_deg = roll_deg[::step], pitch_deg[::step], yaw_deg[::step]

roll  = np.deg2rad(roll_deg)
pitch = np.deg2rad(pitch_deg)
yaw   = np.deg2rad(yaw_deg)

V0, faces = make_box()

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.set_title("Sensor Fusion Method Box (Roll, Pitch, Yaw)")
ax.set_xlim(-2,2); ax.set_ylim(-2,2); ax.set_zlim(-2,2)
ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
ax.grid(True)

poly = Poly3DCollection([], alpha=0.35)
ax.add_collection3d(poly)

# ✅ force initial draw so box appears immediately
R0 = euler_to_R(roll[0], pitch[0], yaw[0])
V_init = (R0 @ V0.T).T
poly.set_verts([[V_init[idx] for idx in f] for f in faces])

def update(i):
    R = euler_to_R(roll[i], pitch[i], yaw[i])
    V = (R @ V0.T).T
    poly.set_verts([[V[idx] for idx in f] for f in faces])
    return (poly,)

ani = FuncAnimation(fig, update, frames=len(roll), interval=30, blit=False)
plt.show()