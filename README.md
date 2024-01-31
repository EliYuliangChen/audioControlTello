# Basic Voice-Controlled Tello Drone

## Overview
This repository contains a basic implementation of voice-controlled commands for operating a Tello drone. The script allows the drone to recognize and respond to a set of predefined commands in English and Chinese. This is achieved using the Vosk speech recognition library and the `djitellopy` library for controlling the Tello drone.

## Prerequisites
- Python 3.x
- `djitellopy` library
- `vosk` library
- `pyaudio` library
- Tello drone
- Vosk model files for English and Chinese

## Installation
1. Install Python 3.x from [Python's official website](https://www.python.org/downloads/).
2. Install the required libraries using pip:  
```pip install djitellopy vosk pyaudio```
3. Download the Vosk model for English and Chinese from the [official Vosk models page](https://alphacephei.com/vosk/models).

## Usage
1. Connect your computer to the Tello drone's Wi-Fi network.
2. Modify the paths to the Vosk model files in the script as per your local setup.
3. Run the script:  
```python voice_control_tello.py```

4. Issue voice commands to control the Tello drone. Supported commands include "take off", "land", "forward", "back", "left", "right", "up", "down", and "flip" in English, and their equivalents in Chinese.

## Extending Functionality
This implementation serves as a basic framework. To extend its functionality or customize it for different use cases, consider:
- Adding more voice commands and corresponding drone actions.
- Improving voice recognition accuracy or adding support for more languages.
- Implementing error handling and response mechanisms for more robust performance.
- Integrating with additional hardware or software for enhanced capabilities.
