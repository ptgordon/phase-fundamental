import numpy as np
import matplotlib.pyplot as plt

# --- Signal Parameters ---
# The signal frequency is 20 kHz, which is much higher than the sampling rate (283 Hz)
# This will result in aliasing, meaning the 20 kHz signal appears at a different frequency
# in the FFT results (specifically, 20000 % 283 = ~242 Hz)
f_signal = 20000.0 # Hz (20 kHz)
Fs = 283.0         # Hz (Sampling rate)
T = 1.0 / Fs       # Sampling period
N = 2048           # Number of samples (FFT size, often a power of 2 for efficiency)

# --- Time Vector and Signal Generation ---
t = np.arange(N) * T # Time vector
# Generate a complex phasor signal: exp(j*2*pi*f*t) = cos(2*pi*f*t) + j*sin(2*pi*f*t)
# We use a real-valued signal here, as the user likely means a physical 20k Hz signal
signal = np.sin(2 * np.pi * f_signal * t)

# --- Compute FFT ---
# Use numpy.fft.fft to get the Fourier coefficients
yf = np.fft.fft(signal) / N  # Normalize by N to get correct amplitude
xf = np.fft.fftfreq(N, T)    # Frequency bins in Hz

# Filter out the symmetric part for real signals and plot only positive frequencies
xf = xf[:N//2]
yf = yf[:N//2]

# --- Calculate Magnitude and Phase ---
magnitude = np.abs(yf)   # Magnitude spectrum
phase = np.angle(yf)     # Phase spectrum (in radians)

# --- Plotting ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Plot Magnitude
ax1.plot(xf, magnitude)
ax1.set_xlim(0, Fs/2) # Nyquist frequency is Fs/2 = 141.5 Hz
ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel('Magnitude')
ax1.set_title(f'Magnitude Spectrum (Sampling Rate: {Fs} Hz)')
ax1.grid()

# Plot Phase
ax2.plot(xf, phase, '.') # Use dots for discrete phase values
ax2.set_xlim(0, Fs/2)
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Phase (Radians)')
ax2.set_title('Phase Spectrum')
ax2.grid()

plt.tight_layout()
plt.show()

