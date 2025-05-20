# Python Voice Assistant

A simple, command-line based voice assistant built in Python. It listens to your voice commands and performs various tasks like searching Wikipedia, opening websites, telling jokes, and more.

## Overview

This voice assistant uses speech recognition to understand spoken commands and text-to-speech to provide responses. It's designed to be a basic framework that can be extended with more functionalities.

## Features

* **Greets User:** Greets the user based on the time of day (Good Morning, Afternoon, Evening).
* **Personalized Interaction:** Asks for the user's name and uses it in interactions.
* **Web Search & Browse:**
    * Searches Wikipedia for a given query and reads out a summary.
    * Opens YouTube.
    * Opens Google.
    * Opens Stack Overflow.
* **Information & Utilities:**
    * Tells the current time.
    * Tells jokes using the `pyjokes` library.
* **Conversation & Interaction:**
    * Responds to "how are you."
    * Acknowledges when the user says they are "fine" or "good."
    * Allows changing the assistant's name.
    * Responds to queries like "what's your name," "who made you," "who are you," "why you came to this world," "what is love," "your purpose."
* **System Interaction (Informational):**
    * Informs the user that actions like "lock window" are OS-specific and provides common shortcuts.
* **Exit:** Allows the user to exit the assistant.
* **Cross-platform Screen Clearing:** Clears the terminal screen at the start.

## Prerequisites

Before you run the assistant, make sure you have the following installed:

1.  **Python:** Version 3.6 or higher is recommended.
2.  **pip:** Python package installer (usually comes with Python).
3.  **Microphone:** A working microphone connected to your computer and configured correctly.
4.  **Internet Connection:** Required for:
    * Speech recognition (uses Google Speech Recognition).
    * Wikipedia searches.
    * Opening web pages.
    * Fetching jokes (if `pyjokes` uses an online source, though often it's local).
5.  **Text-to-Speech (TTS) Engine:**
    * **Windows:** SAPI5 (Usually pre-installed).
    * **macOS:** NSSpeechSynthesizer (Usually pre-installed).
    * **Linux:** eSpeak or Festival. You might need to install one:
        ```bash
        sudo apt-get update
        sudo apt-get install espeak # or festival
        ```

## Installation

1.  **Clone the repository or download the code:**
    Save the Python script as `voice_assistant.py` (or any name you prefer, like `main.py`).

2.  **Create a `requirements.txt` file** in the same directory as your script with the following content:

    ```txt
    pyttsx3
    wikipedia
    pyjokes
    SpeechRecognition
    # shutil, datetime, webbrowser, os are standard libraries
    ```

3.  **Install Python dependencies:**
    Open a terminal or command prompt, navigate to the directory where you saved the files, and run:
    ```bash
    pip install -r requirements.txt
    ```
    * **Microphone Access Issues (Especially on Linux/macOS):** If `SpeechRecognition` has trouble accessing the microphone, you might need to install `PyAudio` (or `portaudio` system libraries):
        ```bash
        # For Debian/Ubuntu based systems (for PyAudio)
        sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
        sudo apt-get install ffmpeg libav-tools
        pip install PyAudio
        ```
        On other systems, consult `PyAudio` installation instructions.

## Running the Assistant

Once the prerequisites and dependencies are set up, you can run the assistant from your terminal:

```bash
python voice_assistant.py
