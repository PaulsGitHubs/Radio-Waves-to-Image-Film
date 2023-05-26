# Radio-Waves-to-Image-Film
This repository contains scripts for converting radio waves into images (frames) and subsequently to film. This transformation is accomplished using a variety of algorithms for image and frame construction.

## Getting Started

Follow these steps to get a copy of the project up and running on your local machine.

### Prerequisites

- Python
- pip
- Git

### Installation

1. Clone the repository:

```bash
git clone https://github.com/PaulsGitHubs/Radio-Waves-to-Image-Film.git
```
2. Navigate to the downloaded folder and install the necessary Python packages:

```bash

cd Radio-Waves-to-Image-Film
pip install -r requirements.txt
```
3. Download the necessary binary files or create your own.

# Visualization

This project outputs every frame in a sequence, according to the chunk size specified in the 2D Cartesian grid scripts. By default, the chunk size is set to half of the input max. The chunk time can be computed as chunk_time = chunk_size / input_max.

Note: 3D visualizations are very computationally intensive. These scripts are not optimized for GPU acceleration, so it is advisable to stick with the 2D Cartesian scripts for better performance.

![Screenshot from 2023-05-25 13-07-28](https://github.com/PaulsGitHubs/Radio-Waves-to-Image-Film/assets/102178068/cdb96dab-ed72-470e-babd-293d88acc63b)



# Compression
For data compression, please refer to our sister project - IQ Sample Compression with FFT and DWT. This project will help you compress the data with DWT, and then decompress it to FFT, IQ samples, etc.

# GNU Radio Companion Usage

The project utilizes GNU Radio Companion (GRC) for handling IQ.bin files. Here's the setup:
- RTL source -> Stream to Vector -> FFT Filter -> File Sink (for the output of the IQ binary file)
- RTL source -> QT GUI Frequency Sink (to visualize what is happening)
![Screenshot from 2023-05-25 13-18-37](https://github.com/PaulsGitHubs/Radio-Waves-to-Image-Film/assets/102178068/356fa74d-42a9-409b-9b6f-10251b33c5d6)

# Data Compression

For data compression, please refer to our sister project - IQ Sample Compression with FFT and DWT. This project will help you compress the data with DWT, and then decompress it to FFT, IQ samples, etc.

#Scripts Included

The repository contains several Python scripts that handle various aspects of the transformation process. These scripts include:
- Script to convert radio frequencies into visible light frequencies
- Script with a PyQt5 UI for file dialogues
- Script for reshaping and normalizing the frequency array
- Script for computing and normalizing the power spectral density
- Script for creating an RGBA image
- Script for combining frequency, PSD, and phase information into image data
- Script to convert visible light frequencies back to radio frequencies
- Script to sort and concatenate .bin files into a single file
- Script to convert images back to .bin files

#Contributing

Contributions, issues and feature requests are welcome! Feel free to check the issues page.
License

# Liscence
This project is licensed under the ____ - see the LICENSE.md file for details.

#Note
Please adjust the links and paths according to your actual repository structure and URLs.

