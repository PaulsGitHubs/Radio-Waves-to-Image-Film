import os
import argparse
import numpy as np
from scipy.fftpack import ifft
import imageio
import matplotlib.colors

# Input frequency range in Hz (hertz)
input_min = 0  # Hz
input_max = 2.048e6  # Hz, assuming RTL-SDR is sampling at 2.4 MHz

# Visible light frequency range in THz (terahertz)
visible_light_min = 430  # THz
visible_light_max = 790  # THz

# Calculate m and b for the linear transformation
m = (visible_light_max - visible_light_min) / (input_max - input_min)
b = visible_light_min - m * input_min

def from_visible_light(visible_light_frequency):
    """Maps a visible light frequency back to the input frequency range."""
    return (visible_light_frequency - b) / m

def main(input_directory, output_directory):
    # Prepare the output directory
    os.makedirs(output_directory, exist_ok=True)
    
    # Process all image files
    for filename in os.listdir(input_directory):
        # Ensure we're processing .png files only
        if not filename.endswith(".png"):
            continue

        # Load the image
        img = imageio.imread(f'{input_directory}/{filename}')

        # Normalize image to the range [0,1]
        img = img / 255.0

        # Convert RGB to HSV
        hsv_image_data = matplotlib.colors.rgb_to_hsv(img[:, :, :3])

        # Recover frequency, PSD, and phase information
        normalized_frequencies = hsv_image_data[:, :, 0]  # Color (hue)
        normalized_psd = hsv_image_data[:, :, 2]  # Brightness
        phase = img[:, :, 3]  # Alpha

        # Denormalize frequencies
        visible_light_frequencies = normalized_frequencies * (visible_light_max - visible_light_min) + visible_light_min
        frequencies = from_visible_light(visible_light_frequencies)

        # Denormalize PSD
        log_psd = normalized_psd * 20 - 40  # assuming log_psd was normalized to [0, 1] and original range was [-40, -20]
        print(f"Max normalized_psd: {np.max(normalized_psd)}, Min normalized_psd: {np.min(normalized_psd)}")
        log_psd = np.clip(log_psd, -709, 709)  # exp(709) is just below the maximum representable float64
        print(f"Max log_psd: {np.max(log_psd)}, Min log_psd: {np.min(log_psd)}")
        psd = np.exp(log_psd)

        # Denormalize phase
        phase = phase * 2 * np.pi

        # Compute magnitudes from PSD
        magnitudes = np.sqrt(psd)

        # Compute complex FFT data from magnitudes and phases
        fft_data = magnitudes * np.exp(1j * phase)

        # Perform inverse FFT to convert frequency domain data back into IQ data
        chunk = ifft(fft_data)

        # Save the recovered IQ data to a file
        chunk.astype(np.complex64).tofile(f'{output_directory}/{filename.replace(".png", ".bin")}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert RGBA images to IQ data.')
    parser.add_argument('-i', '--input', help='Input directory containing the RGBA images.', required=True)
    parser.add_argument('-o', '--output', help='Output directory where the IQ data files will be saved.', required=True)
    args = parser.parse_args()

    main(args.input, args.output)
