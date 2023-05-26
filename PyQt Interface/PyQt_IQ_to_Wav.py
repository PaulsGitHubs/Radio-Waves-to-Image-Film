import numpy as np
from scipy.io import wavfile
from scipy.signal import decimate
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog

class FileDialogDemo(QWidget):
    def __init__(self):
        super().__init__()

        self.title = 'PyQt5 File Dialog'
        self.input_file = None
        self.output_file = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.input_button = QPushButton('Select Input File', self)
        self.input_button.clicked.connect(self.select_input_file)
        layout.addWidget(self.input_button)

        self.output_button = QPushButton('Select Output File', self)
        self.output_button.clicked.connect(self.select_output_file)
        layout.addWidget(self.output_button)

        self.process_button = QPushButton('Process Files', self)
        self.process_button.clicked.connect(self.process_files)
        layout.addWidget(self.process_button)

        self.label = QLabel(self)
        layout.addWidget(self.label)

    def select_input_file(self):
        self.input_file, _ = QFileDialog.getOpenFileName(self, 'Select Input File')
        self.label.setText("Input file selected: " + self.input_file)

    def select_output_file(self):
        self.output_file, _ = QFileDialog.getSaveFileName(self, 'Select Output File')
        self.label.setText("Output file selected: " + self.output_file)

    def process_files(self):
        chunk_size = 1024*1024  # 1 MB, adjust this value to suit your system
        audio_array = np.array([])  # Prepare an array for the audio data

        if self.input_file and self.output_file:
            with open(self.input_file, 'rb') as f:
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
            wavfile.write(self.output_file, 44100, audio_array)
            self.label.setText("Processing done!")
        else:
            self.label.setText("Please select both input and output files.")

def main():
    app = QApplication([])

    demo = FileDialogDemo()
    demo.show()

    app.exec_()

if __name__ == "__main__":
    main()
