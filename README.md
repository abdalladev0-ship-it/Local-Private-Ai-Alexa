# 🚀 Private & Secure Local Alexa Assistant

A fully private, secure, and offline voice-controlled smart assistant clone that runs entirely on your own hardware. By combining local Large Language Models (LLMs) with Python speech processing, this assistant processes all voice requests locally without sending transcripts or audio clips to external cloud servers. 

Features a responsive, high-performance UI consisting of a glowing, pulsing cybernetic Alexa ring that dynamically shifts states (listening, talking, idle) inside a single, dedicated browser tab.

---

## 🛠️ Global Requirements

Before installing the project dependencies, you must install **Ollama** and fetch the optimized lightweight reasoning model on your machine:

1. **Install Ollama:** Follow the steps for your specific Operating System in the installation section below.
2. **Download the Model:** Once Ollama is installed, open your terminal/command prompt and run:
   ```bash
   ollama run qwen2.5:0.5b
   ```
   *(Type `/exit` once the download finishes to return to your standard terminal environment).*

---

## 🚀 Installation & Setup Guide

Select the installation guide below matching your operating system distribution:

### 🪟 Windows Setup
1. **Install Ollama:** Download and run the official installer from [://ollama.com](https://ollama.com).
2. **Install Python:** Ensure Python 3.10+ is installed from the Microsoft Store or official website (Make sure to check the box **"Add Python to PATH"** during installation).
3. Open **PowerShell** or **Command Prompt** and run:
   ```cmd
   python -m venv 8ball-env
   .\8ball-env\Scripts\activate
   pip install SpeechRecognition pyaudio gTTS ollama websockets
   ```
4. Run the assistant:
   ```cmd
   python private_alexa.py
   ```

### 🍎 macOS Setup
1. **Install Ollama:** Download and unzip the application asset from [://ollama.com](https://ollama.com). Launch it to set up terminal commands.
2. Open your **Terminal** application and install system dependencies via Homebrew:
   ```bash
   /bin/bash -c "\$(curl -fsSL https://githubusercontent.com)"
   brew install portaudio flac mpg123
   ```
3. Establish your Python environment and modules:
   ```bash
   python3 -m venv 8ball-env
   source 8ball-env/bin/activate
   pip install SpeechRecognition pyaudio gTTS ollama websockets
   ```
4. Run the assistant:
   ```bash
   python3 private_alexa.py
   ```

### 🐧 Linux Setup (Debian / Ubuntu / Chromebook Linux)
1. **Install Ollama:** Run the automated universal Linux installation script:
   ```bash
   curl -fsSL https://ollama.com | sh
   ```
2. Install underlying audio subsystem packages and drivers:
   ```bash
   sudo apt update && sudo apt install -y portaudio19-dev flac mpg123 python3-pip python3-venv
   ```
3. Set up the secure python local workspace:
   ```bash
   python3 -m venv 8ball-env
   source 8ball-env/bin/activate
   python3 -m pip install SpeechRecognition pyaudio gTTS ollama websockets
   ```
4. Run the assistant:
   ```bash
   python3 private_alexa.py
   ```

### 🦅 Linux Setup (Arch Linux)
1. **Install Ollama:** Pull the package down natively via pacman:
   ```bash
   sudo pacman -S ollama zstd
   sudo systemctl enable --now ollama
   ```
2. Install sound and compiling tools:
   ```bash
   sudo pacman -S portaudio flac mpg123 python-pip
   ```
3. Spin up your Python framework:
   ```bash
   python3 -m venv 8ball-env
   source 8ball-env/bin/activate
   pip install SpeechRecognition pyaudio gTTS ollama websockets
   ```
4. Run the assistant:
   ```bash
   python3 private_alexa.py
   ```

---

## 🎤 Built-in Vocal Automation Commands

Once active, say these specific commands to trigger specialized automation routines:

* **"What time is it?"** -> Dictates the exact live system time out loud.
* **"Open YouTube"** -> Triggers your primary browser to seamlessly navigate to YouTube.
* **"Stop" / "Goodbye"** -> Safely terminates background threads and powers down the listener.
* **[Any generic query or riddle]** -> Directly processed by your private, local local AI model for rapid vocal responses.

---

## 🔒 Absolute Privacy & Data Security
* **Zero Cloud Interaction:** All speech-to-text token processing and AI text generation happen locally inside your system RAM.
* **No Telemetry:** No vocal snippets, logging arrays, or identity markers leave your network architecture.
