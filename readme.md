# Python Not-An-App

This simple text editor application built in Python using the Tkinter library allows users to create, open, edit, and save text files. The application also integrates with Google's GenerativeAI (Gemini) for text generation capabilities.

## Features

- **File Operations:**
  - Create new text files
  - Open existing text files
  - Save edited text files

- **Basic Text Editing:**
  - Cut, Copy, and Paste functionalities
  - Undo and Redo options

- **Google GenerativeAI Integration:**
  - Ask questions prefixed with `-` to interact with a generative model
  - Use `>>` to continue a conversation with context

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/boredom1234/not-an-app.git
    cd not-an-app
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up Google GenerativeAI:

    - Get an API key from [Google GenerativeAI](https://makersuite.google.com/).
    - Replace `'YOUR-API-KEY'` in `notepad.py` with your API key.

## Usage

Run the application:

```bash
python main.py
