import numpy as np
import matplotlib.pyplot as plt
import sys

def main():
# Parameters
    f0 = 20_000          # phasor frequency (Hz)
    fs = 283            # phase sampling rate (Hz)
    phi0 = 0.0          # initial phase (rad)
    duration = 1        # seconds

    if len(sys.argv) > 2:
        f0 = int(sys.argv[1])
        fs = int(sys.argv[2])
    else:
        print("no arguments provided, using defaults of 20 kHz and 283 Hz sample")

    p0 = 1/f0           # period of sampled phasor
    ps = 1/fs           # period of sampler

# we are going to first find the aliasing
    rotations_per_sample = ps/p0 
    observed_rotations_per_sample = rotations_per_sample- np.floor(rotations_per_sample)

    observed_rotations = observed_rotations_per_sample
    iters = 1

# Next we will figure out where the aliasing... aliases
    while observed_rotations <= observed_rotations_per_sample:
        rotations = observed_rotations + observed_rotations_per_sample
        observed_rotations = rotations - np.floor(rotations)
        iters = iters + 1

    print(f"points before inner wrap: {iters}")

    next_corr_point = observed_rotations_per_sample * iters
    next_corr_point = next_corr_point - np.floor(next_corr_point)

    corr_point_movement = next_corr_point - observed_rotations_per_sample
    rec_corr_point_movement = 1/corr_point_movement

    block_wrap = fs/rec_corr_point_movement

    print(f"observed wraps of blocks: {block_wrap}")

# Time samples
    t = np.arange(0, duration, 1/fs)
    colors = ['cyan'] * len(t)

    for i in range(0, len(t), iters-1):
        colors[i] = 'red'

# Phase samples (wrapped to [-pi, pi])
    phase = np.mod(2*np.pi*f0*t + phi0 + np.pi, 2*np.pi) - np.pi

# Plot
    fig, ax = plt.subplots()

    fig.patch.set_facecolor("black")     # figure background
    ax.set_facecolor("black")            # axes background

    ax.scatter(t, phase, c = colors, marker='x')

    ax.plot(t, phase, c = 'cyan')

    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("white")

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Phase (rad)")
    ax.set_title(f"Sampled Phase of {f0/1000:.1f} kHz Phasor at {fs} Hz")
    ax.grid(True)

    plt.show()


if __name__ == "__main__":
    main()
