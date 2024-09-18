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

**For macOS (using Homebrew)**
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

## Available Models and Languages
This framework offers five model sizes, each designed to balance speed and accuracy based on your application's needs. Four of the models are available in English-only versions for tasks requiring better language-specific performance. The models differ in memory requirements and relative speed, allowing flexibility in deployment based on hardware constraints.

Below is a list of available models, their parameter sizes, memory requirements, and relative speeds:

| Model Size | Parameters | English-only Model | Multilingual Model | Required VRAM | Relative Speed |
|------------|------------|--------------------|--------------------|---------------|----------------|
| Tiny       | 39M        | `tiny.en`          | `tiny`             | ~1 GB         | ~32x           |
| Base       | 74M        | `base.en`          | `base`             | ~1 GB         | ~16x           |
| Small      | 244M       | `small.en`         | `small`            | ~2 GB         | ~6x            |
| Medium     | 769M       | `medium.en`        | `medium`           | ~5 GB         | ~2x            |
| Large      | 1550M      | N/A                | `large`            | ~10 GB        | 1x             |

For English-only tasks, we recommend using the `.en` models (e.g., `tiny.en`, `base.en`) as they typically offer better performance. 
The difference in accuracy becomes less significant with the larger models such as small.en and medium.en.


Feel free to adjust based on any additional details you’d like to include.
