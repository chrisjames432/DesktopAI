# DesktopAI

DesktopAI is a desktop application for capturing screenshots, sending them to OpenAI's Vision API, and displaying AI-generated responses in markdown format.

## Features
- Capture screenshots from any connected monitor
- Preview and save screenshots
- Send images to OpenAI Vision API with custom prompts
- View and save AI-generated responses
- Multi-monitor support
- All responses and images are saved locally

## Usage
- **GUI:** Run `python app.py` to launch the Tkinter-based desktop app.
- **CLI:** Run `python oai_imgassistant.py` for command-line image analysis.

## Requirements
- Python 3.8+
- Install dependencies: `pip install -r requirements.txt`
- Create a `.env` file with your OpenAI API key:
  ```
  OPENAIKEY=your_openai_api_key_here
  ```

## File Structure
- `app.py` — Main GUI application
- `oai_imgassistant.py` — Command-line image assistant
- `files/lib.py` — Utility functions
- `files/responses/` — Saved AI responses
- `files/images/` — Saved screenshots

## Notes
- All directories are created automatically at runtime.
- Prompts: Lines starting with `//` are user questions, `/system` sets the system prompt.

---

For more details, see `.github/copilot-instructions.md`.
