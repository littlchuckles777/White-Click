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
currently focused window. Release mouse button 5 to stop scanning.

Use the optional command-line switches to tune the capture behavior without
editing the source code:

```bash
python white_click.py --region-size 30 --threshold 225 --debug
```

- `--region-size`: width/height of the centered capture square in pixels.
- `--threshold`: minimum brightness (0-255) that all RGB channels must reach for
  a pixel to count as “white”. Lower this value if the target never triggers.
- `--poll-interval`: delay between capture attempts while scanning.
- `--cooldown`: pause after emitting `x` before scanning resumes.
- `--debug`: logs the brightest pixel detected in the capture region so you can
  calibrate the threshold.

Press `Ctrl+C` in the terminal to exit the application.

### Calibrating the white detection threshold

Some games and applications add post-processing that keeps the RGB components
below pure white even when the screen “looks” white. Run the script with
`--debug` to view the brightest pixel level (measured as the lowest RGB channel
per pixel) observed in the 20×20 capture region. For example:

```bash
python white_click.py --debug
```

If the log shows values such as `Brightest pixel ... 213/255 (threshold 240)`
while you expect a trigger, restart the script with a lower threshold that still
avoids false positives, e.g. `python white_click.py --threshold 215`.

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

To debug the live capture behavior inside Visual Studio, open the project
properties (**Project** → *project name* Properties → **Debug**) and add any of
the script arguments (for example `--debug --threshold 220`) to the **Script
arguments** field. Starting the debugger (`F5`) will then launch the script with
those options so you can watch the brightness logs in the Visual Studio
Terminal.

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
