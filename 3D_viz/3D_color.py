import os
import numpy as np
from scipy.fft import fft
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors
import skimage.color as color

# Visible light frequency range in THz (terahertz)
visible_light_min = 430  # THz
visible_light_max = 790  # THz

# Input frequency range in Hz (hertz)
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
    iq_data = np.fromfile('input.bin', dtype=np.complex64)

    # Chunk size (in number of samples)
    chunk_size = int(input_max * 0.5)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

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

        # Compute the power spectral density (PSD) and normalize it for brightness adjustment
        psd = np.abs(fft_data) ** 2

        # Apply a logarithmic scale to the PSD to compress the dynamic range,
        # then normalize it for brightness adjustment. Adding a small constant
        # to avoid taking the logarithm of zero.
        log_psd = np.log(psd + 1e-6)
        normalized_psd = (log_psd - np.min(log_psd)) / (np.max(log_psd) - np.min(log_psd))

        # Combine frequency and PSD information
        image_data = np.zeros((len(normalized_frequencies), 3))
        image_data[:, 0] = normalized_frequencies  # Color (hue)
        image_data[:, 1] = 1.0  # Saturation
        image_data[:, 2] = normalized_psd  # Brightness

        # Reshaping the frequency array into 2D format
        size = int(np.sqrt(normalized_frequencies.shape[0]))
        image_data = image_data[:size**2, :].reshape((size, size, 3))

        # Convert HSV to RGB
        rgb_image_data = matplotlib.colors.hsv_to_rgb(image_data)

        # Convert to grayscale and then back to RGB for static
        gray_image_data = color.rgb2gray(rgb_image_data)

        # Reshape normalized_psd to match image_data dimensions
        normalized_psd = normalized_psd[:size**2].reshape((size, size))

        # Replace RGB image data with static data for low PSD values
        gray_image_data[normalized_psd < 0.6] = 0  # zero out the grayscale values where psd is low

        # create a grid for x and y
        X, Y = np.meshgrid(range(size), range(size))

        # create a plane for z (time) at height i
        Z = np.full((size, size), i)

        # Flatten all arrays for scatter plot and ensure all arrays have the same length
        flat_gray_image_data = gray_image_data.flatten()
        X = X.flatten()[:len(flat_gray_image_data)]
        Y = Y.flatten()[:len(flat_gray_image_data)]
        Z = Z.flatten()[:len(flat_gray_image_data)]

        # scatter plot with grayscale color
        ax.scatter(X, Y, Z, c=flat_gray_image_data, cmap='viridis')

    plt.show()
    # Save the plot as a PNG image file
    plt.savefig('3d_plot.png')
if __name__ == "__main__":
    main()
