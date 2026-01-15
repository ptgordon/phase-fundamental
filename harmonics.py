import numpy as np

def spectrum_rfft(x: np.ndarray, fs: float, window: str = "hann"):
    x = np.asarray(x)
    x = x - np.mean(x)  # remove DC

    if window == "hann":
        w = np.hanning(len(x))
    elif window is None:
        w = np.ones(len(x))
    else:
        raise ValueError("window must be 'hann' or None")

    X = np.fft.rfft(x * w)
    f = np.fft.rfftfreq(len(x), d=1/fs)

    # amplitude correction for window (rough but useful)
    # For Hann, coherent gain is 0.5; for rectangular, 1.0
    cg = 0.5 if window == "hann" else 1.0
    mag = (2.0 / (len(x) * cg)) * np.abs(X)
    phase = np.angle(X)
    return f, X, mag, phase

def find_fundamental(f, mag, fmin=0.1):
    # ignore DC and very low freq bins
    idx0 = np.searchsorted(f, fmin)
    k = idx0 + np.argmax(mag[idx0:])
    return k, f[k]

def list_harmonics(f, X, f1, n_harmonics=10, search_bins=1):
    """
    For each k*f1, look in a small neighborhood of FFT bins to grab the largest bin.
    Returns list of dicts with harmonic number, freq, amplitude, phase.
    """
    out = []
    nyq = f[-1]
    for k in range(1, n_harmonics + 1):
        target = k * f1
        if target > nyq:
            break
        i = int(np.argmin(np.abs(f - target)))
        lo = max(0, i - search_bins)
        hi = min(len(f) - 1, i + search_bins)
        j = lo + np.argmax(np.abs(X[lo:hi+1]))
        out.append({
            "harmonic": k,
            "freq_hz": float(f[j]),
            "amplitude": float((2.0 / len(X)) * np.abs(X[j])),  # uncalibrated-ish, but comparable
            "phase_rad": float(np.angle(X[j])),
        })
    return out

# --- Example usage ---
if __name__ == "__main__":
    fs = 113.0
    f0 = 1_200.0
    T = 4.0
    t = np.arange(0, T, 1/fs)

    # Example 1: aliased real waveform (will show one dominant tone)
    x = np.cos(2*np.pi*f0*t)

    # Example 2: wrapped phase sawtooth (uncomment to analyze this instead)
    # phase = (2*np.pi*f0*t) % (2*np.pi)  # [0, 2pi)
    # x = phase

    f, X, mag, ph = spectrum_rfft(x, fs, window="hann")
    kfund, f1 = find_fundamental(f, mag, fmin=0.1)

    print(f"Fundamental ≈ {f1:.3f} Hz (FFT bin {kfund})")

    harms = list_harmonics(f, X, f1, n_harmonics=20, search_bins=1)
    print("\nHarmonics:")
    for h in harms:
        print(f"{h['harmonic']:2d}x  {h['freq_hz']:8.3f} Hz   amp={h['amplitude']:.4g}   phase={h['phase_rad']:+.3f} rad")

