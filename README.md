# G.Writer - AI Text Rewriter

A Windows GUI application that uses Google Gemini AI to rewrite and improve text with a simple Alt+G hotkey.

## Features

- **Global Hotkey**: Press Alt+G anywhere to rewrite selected text
- **Google Gemini Integration**: Powered by Google's Generative AI
- **System Tray**: Runs quietly in the background
- **GUI Configuration**: Easy API key setup and management
- **Windows Integration**: Works with any text selection in any application

## Installation

### Option 1: Download Executable (Recommended)
1. Download `G.Writer.exe` from the [releases](../../releases) or `dist/` folder
2. Run the executable - no installation required!
3. Configure your Google Gemini API key in the GUI
4. Press Alt+G to rewrite selected text anywhere

### Option 2: Run from Source
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python g_writer.py`

## Setup

1. Get a free Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Launch G.Writer and enter your API key
3. Click "Verify API Key" to test the connection
4. Click "Save" to store your key
5. The app will minimize to system tray

## Usage

1. Select any text in any application (browser, Word, notepad, etc.)
2. Press **Alt+G**
3. The selected text will be automatically rewritten and replaced

## Requirements

- Windows 10/11
- Google Gemini API key (free)
- Internet connection

## Dependencies

- `google-generativeai` - Google Gemini AI integration
- `tkinter` - GUI framework (built into Python)
- `pystray` - System tray functionality
- `pyautogui` - Keyboard automation
- `pynput` - Global hotkey detection
- `pywin32` - Windows clipboard access

## Building Executable

To build your own executable:

```bash
pip install pyinstaller
pyinstaller g_writer.spec
```

The executable will be created in the `dist/` folder.

## License

Open source - feel free to modify and distribute.

---

**Built with ❤️ and AI assistance**