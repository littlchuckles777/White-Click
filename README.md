# White-Click

A low-latency utility that continuously monitors a 20×20 square in the center of
your primary monitor and sends an `x` keypress whenever pure white pixels are
detected while you hold mouse button 5 (typically the forward side button).

## Requirements

- Python 3.9+
- [mss](https://github.com/BoboTiG/python-mss)
- [numpy](https://numpy.org/)
- [pynput](https://github.com/moses-palmer/pynput)

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Run the clicker from a terminal:

```bash
python white_click.py
```

Hold mouse button 5 to enable scanning. When pure white pixels are detected
within the capture region, the script immediately emits an `x` keypress to the
currently focused window.
Release mouse button 5 to stop scanning.

Press `Ctrl+C` in the terminal to exit the application.

### Adjusting the capture region size

The size of the monitored region is controlled by the `region_size` argument of
`WhiteClicker` in `white_click.py`. By default, the application instantiates
`WhiteClicker()` without arguments, which watches a 20×20 pixel square centered
on the primary monitor. To use a different size, open `white_click.py` and adjust
the value passed when `WhiteClicker` is created at the bottom of the file:

```python
if __name__ == "__main__":
    WhiteClicker(region_size=40).start()
```

Replace `40` with the number of pixels you want for both the width and height of
the square capture region.

## Building an Executable in VS Code

1. Install the **Python** and **Python Debugger** extensions in VS Code.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\\Scripts\\activate
   ```
3. Install the runtime dependencies and build tools:
   ```bash
   pip install -r requirements.txt pyinstaller
   ```
4. Open the repository folder in VS Code and select the virtual environment as the
   interpreter (`Ctrl+Shift+P` → **Python: Select Interpreter** → `.venv`).
5. Build a standalone executable with PyInstaller:
   ```bash
   pyinstaller --onefile --name white_click white_click.py
   ```
   The resulting executable will be located in `dist/white_click` (or
   `dist\white_click.exe` on Windows).

## Building an Executable in Visual Studio

1. Install Visual Studio 2022 with the **Python development** workload.
2. Create a new **Python Application** solution and add the contents of this
   repository to the project.
3. Open the **Python Environments** window, create a new virtual environment for
   the project, and install the requirements along with PyInstaller:
   ```powershell
   pip install -r requirements.txt pyinstaller
   ```
4. Open the **Command Prompt** (from the Visual Studio terminal or Windows
   Terminal) with the project's virtual environment activated and run:
   ```powershell
   pyinstaller --onefile --name white_click white_click.py
   ```
5. Retrieve the generated executable from the `dist` directory inside the
   project folder.

## Obfuscating with PyArmor

1. Install PyArmor in the same environment used for building:
   ```bash
   pip install pyarmor
   ```
2. Generate the obfuscated package while keeping the original entry point:
   ```bash
   pyarmor gen -O dist/obf white_click.py
   ```
3. Run the obfuscated script directly with Python:
   ```bash
   python dist/obf/white_click.py
   ```
4. Bundle the protected sources into an executable using the provided
   PyInstaller spec file, which automatically includes the PyArmor runtime and
   the hidden imports that PyInstaller cannot infer from the obfuscated entry
   point:
   ```bash
   pyinstaller white_click_obf.spec
   ```
   The executable is emitted to `dist/white_click_obf` (or
   `dist\white_click_obf.exe` on Windows). The obfuscated sources remain in
   `dist/obf` for inspection or rebuilding later.
