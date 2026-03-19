import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ACCEL_CSV = "accel_dynamic.csv"  # change to your filename

def euler_to_R(roll, pitch):
    cr, sr = np.cos(roll), np.sin(roll)
    cp, sp = np.cos(pitch), np.sin(pitch)

    Ry = np.array([[ cp, 0, sp],
                   [  0, 1,  0],
                   [-sp, 0, cp]])
    Rx = np.array([[1,  0,   0],
                   [0, cr, -sr],
                   [0, sr,  cr]])
    return Ry @ Rx

def make_box(size=(1.4, 0.9, 0.7)):
    lx, ly, lz = size
    x, y, z = lx/2, ly/2, lz/2
    V = np.array([
        [-x,-y,-z],[ x,-y,-z],[ x, y,-z],[-x, y,-z],
        [-x,-y, z],[ x,-y, z],[ x, y, z],[-x, y, z],
    ])
    faces = [[0,1,2,3],[4,5,6,7],[0,1,5,4],[2,3,7,6],[1,2,6,5],[0,3,7,4]]
    return V, faces

# ---- Read CSV (skip header if it exists) ----
df = pd.read_csv(ACCEL_CSV, header=None, skiprows=1)

# If first row contains words, drop it
if df.iloc[0].astype(str).str.contains("roll|pitch|time|method", case=False).any():
    df = df.iloc[1:].reset_index(drop=True)

df = df.dropna(subset=[0,1,2,3,4])

roll  = pd.to_numeric(df.iloc[:, 2], errors="coerce").to_numpy()
pitch = pd.to_numeric(df.iloc[:, 3], errors="coerce").to_numpy()

mask = np.isfinite(roll) & np.isfinite(pitch)
roll, pitch = roll[mask], pitch[mask]

print("Samples:", len(roll))

# downsample for smoother animation
step = max(1, len(roll)//500)
roll, pitch = roll[::step], pitch[::step]

V0, faces = make_box()

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.set_title("Accelerometer Box (Yaw=0, Roll & Pitch only)")
ax.set_xlim(-2,2); ax.set_ylim(-2,2); ax.set_zlim(-2,2)
ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
ax.grid(True)

poly = Poly3DCollection([], alpha=0.35)
ax.add_collection3d(poly)

# ✅ Force initial box draw
R0 = euler_to_R(np.deg2rad(roll[0]), np.deg2rad(pitch[0]))
V_init = (R0 @ V0.T).T
poly.set_verts([[V_init[idx] for idx in f] for f in faces])

def update(i):
    R = euler_to_R(np.deg2rad(roll[i]), np.deg2rad(pitch[i]))
    V = (R @ V0.T).T
    poly.set_verts([[V[idx] for idx in f] for f in faces])
    return (poly,)

# ✅ Keep a reference to animation
ani = FuncAnimation(fig, update, frames=len(roll), interval=30, blit=False)

plt.show()