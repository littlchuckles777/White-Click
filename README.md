# White-Click

A low-latency utility that continuously monitors a 50×50 square in the center of
your primary monitor and performs a left click whenever pure white pixels are
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
within the capture region, the script immediately performs a left click.
Release mouse button 5 to stop scanning.

Press `Ctrl+C` in the terminal to exit the application.
