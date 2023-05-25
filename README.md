# Radio-Waves-to-Image-Film
This repo allows people to transform radiowaves from channels they pick to images (frames) then film based on a some algorithms for image/frame construction

# Requirements
Clone repo
Download the binary files or take some on your own...

# Visualization

So every frame is output in a sequence according to chunk size set on the 2D_cartesian_grid scripts. By default it is set to half of input max... for chunk time we can do chunk_time = chunk_size / input_max... I will update script with this so it is more straight forward when running... for a short IQ binary file it would look like this.

![Screenshot from 2023-05-25 13-07-28](https://github.com/PaulsGitHubs/Radio-Waves-to-Image-Film/assets/102178068/cdb96dab-ed72-470e-babd-293d88acc63b)

Keep in mind running 3D visualizations are very computationally intensive, and I would suggest sticking to the 2D cartesian scripts... even if you have a supercomputer, these are not optamized for GPU acceleration... so just stick with the 2D visualizations for now... trust me.

# GNU Radio Companion Setup for IQ.bin files

RTL source -> Stream to Vector -> FFT Filter -> File Sink (for the output of the IQ binary file)
RTL source -> QT GUI Frequency Sink (to visualize what is happening)
![Screenshot from 2023-05-25 13-18-37](https://github.com/PaulsGitHubs/Radio-Waves-to-Image-Film/assets/102178068/356fa74d-42a9-409b-9b6f-10251b33c5d6)


# Compression
Please go to https://github.com/PaulsGitHubs/IQ-Sample-Compression-with-FFT-and-DWT for compressing the data. You will be able to compress it with DWT, then decompress it to FFT, IQ samples, etc :)

:)))

Fun stuff :)
