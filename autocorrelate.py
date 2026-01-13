import numpy as np
import matplotlib.pyplot as plt

# Parameters
f0 = 20_000
fs = 283
duration = 1.0

t = np.arange(0, duration, 1/fs)
x = np.cos(2*np.pi*f0*t)

# FFT
X = np.fft.rfft(x * np.hanning(len(x)))
freqs = np.fft.rfftfreq(len(x), d=1/fs)

# Peak frequency
idx = np.argmax(np.abs(X))
f_est = freqs[idx]

print(f"Estimated fundamental (FFT): {f_est:.2f} Hz")

# Plot
plt.plot(freqs, np.abs(X))
plt.axvline(f_est, color='r', linestyle='--')
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("FFT of Undersampled Waveform")
plt.grid(True)
plt.show()
