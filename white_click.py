"""White pixel activation application.

This script monitors the center portion of the primary monitor for pure white
pixels while the user holds mouse button 5 (typically the forward side button).
When white pixels are detected within the watched region, the script emits a
Left Alt keyboard input once per activation. Low latency is prioritized by
minimizing the amount of work performed per capture.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Optional

import numpy as np
from mss import mss
from mss.exception import ScreenShotError
from pynput import keyboard, mouse


@dataclass(frozen=True)
class CaptureRegion:
    """Represents the screen region that should be monitored."""

    left: int
    top: int
    width: int
    height: int


class WhiteClicker:
    """Monitors for white pixels while the user holds mouse button 5."""

    def __init__(
        self,
        region_size: int = 50,
        poll_interval: float = 0.005,
        click_cooldown: float = 0.025,
    ) -> None:
        self._region_size = max(1, region_size)
        self._poll_interval = max(0.001, poll_interval)
        self._click_cooldown = max(0.0, click_cooldown)

        self._listener: Optional[mouse.Listener] = None
        self._active = False
        self._active_event = threading.Event()
        self._stop_event = threading.Event()
        self._keyboard = keyboard.Controller()
        self._triggered_this_hold = False

    @staticmethod
    def _compute_center_region(screen_capture: mss, region_size: int) -> CaptureRegion:
        """Compute a capture region centered on the primary monitor."""

        monitor = screen_capture.monitors[1]  # Primary monitor
        half = region_size // 2
        center_x = monitor["left"] + monitor["width"] // 2
        center_y = monitor["top"] + monitor["height"] // 2

        return CaptureRegion(
            left=center_x - half,
            top=center_y - half,
            width=region_size,
            height=region_size,
        )

    def _on_click(self, _x: int, _y: int, button: mouse.Button, pressed: bool) -> None:
        if button == mouse.Button.x2:
            self._active = pressed
            if pressed:
                self._active_event.set()
                print("Mouse button 5 detected as held.")
                self._triggered_this_hold = False
            else:
                self._active_event.clear()
                self._triggered_this_hold = False

    def _capture_has_white(self, sct, region: CaptureRegion) -> bool:
        raw = sct.grab(
            {
                "left": region.left,
                "top": region.top,
                "width": region.width,
                "height": region.height,
            }
        )

        # Convert the BGRA buffer to a NumPy array without copying when possible.
        frame = np.asarray(raw, dtype=np.uint8)
        # Check if any pixel is pure white (255, 255, 255) regardless of alpha.
        rgb = frame[:, :, :3]
        has_white = np.all(rgb == 255, axis=2).any()
        if has_white:
            print("White detected in capture region.")
        return has_white

    def _send_left_alt(self) -> None:
        self._keyboard.press(keyboard.Key.alt_l)
        time.sleep(0.01)
        self._keyboard.release(keyboard.Key.alt_l)
        print("Left Alt input sent.")

    def _loop(self) -> None:
        sct = None
        region: Optional[CaptureRegion] = None

        try:
            while not self._stop_event.is_set():
                if not self._active_event.wait(timeout=self._poll_interval):
                    if not self._active and sct is not None:
                        sct.close()
                        sct = None
                        region = None
                    continue

                if not self._active:
                    continue

                if sct is None:
                    sct = mss()
                    region = self._compute_center_region(sct, self._region_size)

                try:
                    if region and self._capture_has_white(sct, region):
                        if not self._triggered_this_hold:
                            self._send_left_alt()
                            self._triggered_this_hold = True
                            if self._click_cooldown:
                                time.sleep(self._click_cooldown)
                            continue
                except (AttributeError, ScreenShotError):
                    # Re-create the MSS session if the underlying handles were lost.
                    sct.close()
                    sct = None
                    region = None
                    continue

                time.sleep(self._poll_interval)
        finally:
            if sct is not None:
                sct.close()

    def start(self) -> None:
        if self._listener is not None:
            raise RuntimeError("WhiteClicker is already running")

        self._stop_event.clear()
        self._active_event.clear()
        self._active = False

        self._listener = mouse.Listener(on_click=self._on_click)
        self._listener.start()

        worker = threading.Thread(target=self._loop, daemon=True)
        worker.start()

        try:
            while worker.is_alive():
                worker.join(timeout=0.1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self) -> None:
        self._active = False
        self._stop_event.set()
        self._active_event.set()
        if self._listener is not None:
            self._listener.stop()
            self._listener = None


if __name__ == "__main__":
    clicker = WhiteClicker(region_size=50)
    clicker.start()
