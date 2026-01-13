import numpy as np
import matplotlib.pyplot as plt
import sys

def main():
# Parameters
    f0 = 20_000          # phasor frequency (Hz)
    fs = 283            # phases sampling rate (Hz)
    phi0 = 0.0          # initial phases (rad)
    duration = 1        # seconds

    if len(sys.argv) > 2:
        f0 = int(sys.argv[1])
        fs = int(sys.argv[2])
    else:
        print("no arguments provided, using defaults of 20 kHz and 283 Hz sample")

    t = np.arange(0, duration, 1/fs)
    phases = np.mod(2*np.pi*f0*t + phi0 + np.pi, 2*np.pi) - np.pi
    # phases = np.mod(2*np.pi*f0*t, 2*np.pi)
    print(f"{phases}")

    iters = 1
    first_phase = phases[1]

    for phase in phases[1:]:
        iters = iters+1
        if abs(phase) < abs(first_phase):
            break

    print(f"points before inner wrap: {iters}")

    next_corr_point = phases[iters-1]
    print(f"{next_corr_point}")

    corr_point_movement = abs(phases[1]) - abs(next_corr_point) 

    rec_corr_point_movement = phases[1]/(np.pi/corr_point_movement)

    block_wrap = fs/rec_corr_point_movement

    print(f"observed wraps of blocks: {block_wrap}")

# Time samples
    colors = ['cyan'] * len(t)

    for i in range(0, len(t), iters-1):
        colors[i] = 'red'

# phases samples (wrapped to [-pi, pi])
    x = np.cos(2*np.pi*f0*t)

# FFT
    X = np.fft.rfft(x * np.hanning(len(x)))
    freqs = np.fft.rfftfreq(len(x), d=1/fs)

# Peak frequency
    idx = np.argmax(np.abs(X))
    f_est = freqs[idx]


# Peak frequency
    idx = np.argmax(np.abs(X))
    f_est = freqs[idx]

    print(f"Estimated fundamental (FFT): {f_est:.2f} Hz")


# Plot
    fig, ax = plt.subplots()

    fig.patch.set_facecolor("black")     # figure background
    ax.set_facecolor("black")            # axes background

    ax.scatter(t, phases, c = colors, marker='x')

    ax.plot(t, phases, c = 'cyan')

    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("white")

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("phases (rad)")
    ax.set_title(f"Sampled phases of {f0/1000:.1f} kHz Phasor at {fs} Hz")
    ax.grid(True)

    plt.show()


if __name__ == "__main__":
    main()
