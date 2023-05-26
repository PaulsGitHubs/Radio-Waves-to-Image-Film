import numpy as np
from scipy.io import wavfile
from scipy.signal import decimate

# Define the chunk size
chunk_size = 1024*1024  # 1 MB, adjust this value to suit your system

# Prepare an array for the audio data
audio_array = np.array([])

# Process the file in chunks
with open('input.bin', 'rb') as f:
    while True:
        # Read chunk from file
        chunk_complex = np.fromfile(f, dtype=np.complex64, count=chunk_size)

        # If chunk is smaller than chunk_size, we've reached the end of the file
        if chunk_complex.size < chunk_size:
            break

        # Calculate the instantaneous phase difference (proportional to frequency) of the complex samples
        instantaneous_phase = np.unwrap(np.angle(chunk_complex))
        audio = np.diff(instantaneous_phase)

        # We are assuming that the original sample rate was 2.048 MHz.
        # Decimate to 44.1 kHz for the WAV file.
        decimation_factor = int(2.048e6 // 44100)

        # Decimate the signal
        audio_decimated = decimate(audio, decimation_factor, ftype='fir')

        # Normalize the audio to the range -32767 to 32767 for a 16-bit WAV file
        audio_normalized = np.int16(audio_decimated / np.max(np.abs(audio_decimated)) * 32767)

        # Append to audio array
        audio_array = np.concatenate((audio_array, audio_normalized))

# Write the audio data to the WAV file
wavfile.write('output.wav', 44100, audio_array)

