import unittest

from .base import BaseGUITestCase


class SmokeTest(BaseGUITestCase):
    def test_launches(self):
        self.save_screenshot()
        self.assertFalse(self.gui_proc.poll())

    def test_open_terminal(self):
        self.save_screenshot()

        with self.async_sikuli_script('open_terminal.sikuli') as proc:
            while proc.poll() is None:
                self.save_screenshot()
                import time
                time.sleep(0.5)

        self.save_screenshot()
