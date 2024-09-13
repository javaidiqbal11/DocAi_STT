# DoctorAI - Speech to Text and Text to Speech
DoctorAI is a Python-based tool that leverages offline dictionaries to perform speech-to-text (STT) and text-to-speech (TTS) tasks, including support for health-related terminology. The project ensures privacy by functioning offline and incorporates medical-specific vocabulary for enhanced accuracy in healthcare applications.

## Requirements
- `Python 3.10`
- Offline STT/TTS Libraries
- FFmpeg (for audio processing)

## Installation
Install Python Dependencies
To install the required Python packages, navigate to the project directory and run:

```shell
pip install -r requirements.txt
```
## Install FFmpeg
Make sure FFmpeg is installed and available in the current directory or on your system's PATH. You can download FFmpeg from the official site here.

If you're on Linux or macOS, you can install FFmpeg using the package manager:

**For Ubuntu/Linux**
```shell
sudo apt-get install ffmpeg
```

# For macOS (using Homebrew)
```shell
brew install ffmpeg
```

**On Windows**
Download and place the FFmpeg executable in the current directory or add it to your system's PATH.

## Usage
To run the DoctorAI STT system, use the following command:

```shell
python DocAi_STT.py
```
This will start the speech-to-text process using offline resources.

Feel free to adjust based on any additional details you’d like to include.
