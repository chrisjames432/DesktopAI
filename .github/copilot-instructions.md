# Copilot Instructions for DesktopAI

## Project Overview
- **DesktopAI** is a desktop application (Tkinter GUI) for capturing screenshots, sending them to OpenAI's Vision API, and displaying AI-generated responses in markdown.
- The app supports multi-monitor setups, image preview, and saving both images and AI responses.
- Key files:
  - `app.py`: Main GUI, screenshot logic, OpenAI API streaming, file management.
  - `oai_imgassistant.py`: CLI utility for image analysis via OpenAI Vision.
  - `files/lib.py`: Utility functions for file, JSON, and DB operations.
  - `files/responses.txt`: Example AI responses (not code-driven).

## Architecture & Data Flow
- **User Workflow:**
  1. User selects a monitor and takes a screenshot (auto or manual).
  2. Screenshot is encoded and sent to OpenAI Vision API with a system/user prompt.
  3. Streaming response is displayed live in the GUI and can be saved.
  4. Images and responses are saved in `files/images/` and `files/responses/`.
- **Threading** is used for non-blocking API calls and screenshot capture.
- **Environment variables** (API keys) are loaded via `dotenv`.
- **No build step**; run with `python app.py` (GUI) or `python oai_imgassistant.py` (CLI).

## Conventions & Patterns
- **Responses** are saved as text files with random filenames in `files/responses/`.
- **Images** are saved as `.jpg` in `files/images/`.
- **System/user prompts** are entered in the GUI; lines starting with `//` are treated as user questions, `/system` for system prompt.
- **Tkinter** is used for all UI; avoid introducing other GUI frameworks.
- **All file and directory creation** is handled at runtime; no manual setup needed.
- **Utilities** in `files/lib.py` are used for JSON, file, and DB operations—prefer these over re-implementing helpers.

## Integration & Extensibility
- **OpenAI Vision API** is the only external AI integration (via `openai` Python package).
- **.env** file required for `OPENAIKEY`.
- **No test suite** or CI/CD currently present.
- **No custom build, lint, or test commands**—run scripts directly.

## Examples
- To add a new response type, save to `files/responses/` using the `save_to_file` pattern in `app.py`.
- To add a new utility, extend `files/lib.py` and import as needed.

---

For questions or unclear conventions, review `app.py` for main flows and `files/lib.py` for helpers. Ask for clarification if a workflow or pattern is not obvious from these files.
