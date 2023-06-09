import os
import numpy as np
from scipy.fft import fft
import matplotlib.pyplot as plt
import matplotlib
# Visible light frequency range in THz (terahertz)
visible_light_min = 430  # THz
visible_light_max = 790  # THz

# Input frequency range in Hz (hertz)
# You might want to adjust these values based on the actual input range from the RTL-SDR
input_min = 0  # Hz
input_max = 2.048e6  # Hz, assuming RTL-SDR is sampling at 2.4 MHz

# Calculate m and b for the linear transformation
m = (visible_light_max - visible_light_min) / (input_max - input_min)
b = visible_light_min - m * input_min

def to_visible_light(input_frequency):
    """Maps an input frequency to the visible light frequency range."""
    return m * input_frequency + b

def main():
    # Load the RTL-SDR data from a file
    # Replace this with the actual file path and loading method
    iq_data = np.fromfile('input.bin', dtype=np.complex64)

    # Chunk size (in number of samples)
    chunk_size = int(input_max * 0.5)  # This should give chunks of 0.2 seconds each, adjust as needed

    # Prepare the pictures directory
    os.makedirs('frames_Mag_Norm', exist_ok=True)

    for i in range(len(iq_data)//chunk_size):
        # Select the current chunk
        chunk = iq_data[i*chunk_size:(i+1)*chunk_size]

        # Perform FFT to convert IQ data into frequency domain
        fft_data = fft(chunk)
        frequencies = np.fft.fftfreq(len(chunk)) * input_max

        # Apply the transformation to each frequency
        visible_light_frequencies = to_visible_light(np.abs(frequencies))

        # Normalizing frequencies to 0-1 range for color mapping
        normalized_frequencies = (visible_light_frequencies - np.min(visible_light_frequencies)) / np.ptp(visible_light_frequencies)

        # Compute the magnitude of the FFT data and normalize it for brightness adjustment
        normalized_magnitude = np.abs(fft_data) / np.max(np.abs(fft_data))

        # Combine frequency and magnitude information
        image_data = np.zeros((len(normalized_frequencies), 3))
        image_data[:, 0] = normalized_frequencies  # Color (hue)
        image_data[:, 1] = 1.0  # Saturation
        image_data[:, 2] = normalized_magnitude  # Brightness

        # Reshaping the frequency array into 2D format
        size = int(np.sqrt(normalized_frequencies.shape[0]))
        image_data = image_data[:size**2, :].reshape((size, size, 3))

        # Convert HSV to RGB
        image_data = matplotlib.colors.hsv_to_rgb(image_data)

        # Create the image
        plt.imshow(image_data)
        plt.axis('off')

        # Save the image
        plt.savefig(f'frames_Mag_Norm/frame_{i:04d}.png', bbox_inches='tight', pad_inches=0)
        plt.clf()  # Clear the current figure's content

if __name__ == "__main__":
    main()
