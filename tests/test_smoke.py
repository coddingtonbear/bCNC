import shutil
import time

import pyautogui

from .base import BaseGUITestCase


class SmokeTest(BaseGUITestCase):
    def test_launches(self):
        self.assertFalse(self.gui_proc.poll())

    def test_can_load_and_run_sample_gcode(self):
        shutil.copy(
            self.get_static_path('sample.gcode'),
            '/tmp/',
        )

        self.save_screenshot()
        self.send_command('load /tmp/sample.gcode')
        self.save_screenshot()
        pyautogui.press('f10')  # Mapped to 'start' in config
        for _ in range(10):
            self.save_screenshot()
            time.sleep(1)
        pyautogui.press('f12')  # Mapped to 'stop' in config
        for _ in range(10):
            self.save_screenshot()
            time.sleep(1)
        self.save_screenshot()

        print(self.get_bcnc_state())
        self.assertTrue(
            'Alarm' in self.get_bcnc_state()['state']
        )
