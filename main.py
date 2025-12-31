import numpy as np
import matplotlib.pyplot as plt

# Parameters
f0 = 20_000        # phasor frequency (Hz)
fs = 279          # phase sampling rate (Hz)
phi0 = 0.0         # initial phase (rad)
duration = 1        # seconds

# Time samples
t = np.arange(0, duration, 1/fs)

# Phase samples (wrapped to [-pi, pi])
phase = np.mod(2*np.pi*f0*t + phi0 + np.pi, 2*np.pi) - np.pi

# Plot


fig, ax = plt.subplots()

fig.patch.set_facecolor("black")     # figure background
ax.set_facecolor("black")            # axes background

ax.plot(t, phase, color="cyan", marker='x')

ax.tick_params(colors="white")
ax.xaxis.label.set_color("white")
ax.yaxis.label.set_color("white")
ax.title.set_color("white")

ax.set_xlabel("Time (s)")
ax.set_ylabel("Phase (rad)")
ax.set_title(f"Sampled Phase of {f0/1000:.1f} kHz Phasor at {fs} Hz")
ax.grid(True)

plt.show()
