import unittest

from .base import BaseGUITestCase


class SmokeTest(BaseGUITestCase):
    def test_launches(self):
        self.save_screenshot()
        self.assertFalse(self.gui_proc.poll())

    def test_open_terminal(self):
        import time
        self.save_screenshot()

        timeout = time.time() + 30
        with self.async_sikuli_script('open_terminal.sikuli') as proc:
            while not proc.poll():
                self.save_screenshot()
                time.sleep(500)

                if time.time() > timeout:
                    print "TIMEOUT"
                    break

        self.save_screenshot()
