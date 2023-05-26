import os
import re
import numpy as np
from scipy.fftpack import ifft
import imageio
import matplotlib.colors
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog

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

def numerical_sort(filenames):
    """
    Sorts the given iterable in the way that humans expect.
    (i.e., 'frame10.bin' comes after 'frame2.bin')
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(filenames, key=alphanum_key)

def concatenate_files(input_directory, output_file):
    filenames = []
    for filename in numerical_sort(os.listdir(input_directory)):
        if filename.endswith(".bin"):
            filenames.append(os.path.join(input_directory, filename))
    with open(output_file, 'wb') as outfile:
        for filename in filenames:
            with open(filename, 'rb') as readfile:
                outfile.write(readfile.read())

class FileDialogDemo(QWidget):
    def __init__(self):
        super().__init__()

        self.title = 'PyQt5 File Dialog'
        self.input_directory = None
        self.output_directory = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.input_button = QPushButton('Select Input Directory', self)
        self.input_button.clicked.connect(self.select_input_directory)
        layout.addWidget(self.input_button)

        self.output_button = QPushButton('Select Output Directory', self)
        self.output_button.clicked.connect(self.select_output_directory)
        layout.addWidget(self.output_button)

        self.process_button = QPushButton('Process Files', self)
        self.process_button.clicked.connect(self.process_files)
        layout.addWidget(self.process_button)

        self.label = QLabel(self)
        layout.addWidget(self.label)

    def select_input_directory(self):
        self.input_directory = QFileDialog.getExistingDirectory(self, 'Select Input Directory')
        self.label.setText("Input directory selected: " + self.input_directory)

    def select_output_directory(self):
        self.output_directory = QFileDialog.getExistingDirectory(self, 'Select Output Directory')
        self.label.setText("Output directory selected: " + self.output_directory)

    def process_files(self):
        if self.input_directory is not None and self.output_directory is not None:
            os.makedirs(self.output_directory, exist_ok=True)
            for filename in os.listdir(self.input_directory):
                if not filename.endswith(".png"):
                    continue
                img = imageio.imread(f'{self.input_directory}/{filename}')
                img = img / 255.0
                hsv_image_data = matplotlib.colors.rgb_to_hsv(img[:, :, :3])
                normalized_frequencies = hsv_image_data[:, :, 0]
                normalized_psd = hsv_image_data[:, :, 2]
                phase = img[:, :, 3]
                visible_light_frequencies = normalized_frequencies * (visible_light_max - visible_light_min) + visible_light_min
                frequencies = from_visible_light(visible_light_frequencies)
                log_psd = normalized_psd * 20 - 40
                log_psd = np.clip(log_psd, -709, 709)
                psd = np.exp(log_psd)
                phase = phase * 2 * np.pi
                magnitudes = np.sqrt(psd)
                fft_data = magnitudes * np.exp(1j * phase)
                chunk = ifft(fft_data)
                chunk.astype(np.complex64).tofile(f'{self.output_directory}/{filename.replace(".png", ".bin")}')
            
            # After converting all images to .bin files, concatenate them into a single file
            concatenate_files(self.output_directory, os.path.join(self.output_directory, 'combined.bin'))
            self.label.setText("Processing done!")
        else:
            self.label.setText("Please select both input and output directories.")

def main():
    app = QApplication([])

    demo = FileDialogDemo()
    demo.show()

    app.exec_()

if __name__ == "__main__":
    main()
