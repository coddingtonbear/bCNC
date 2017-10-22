import shutil
import time

from .base import BaseGUITestCase


class SmokeTest(BaseGUITestCase):
    def test_launches(self):
        self.assertFalse(self.gui_proc.poll())

    def test_can_open_terminal(self):
        self.run_sikuli_script('open_terminal.sikuli')

    def test_can_load_and_run(self):
        shutil.copy(
            self.get_static_path('sample.gcode'),
            '/tmp/',
        )

        with self.async_sikuli_script(
            'run_sample_gcode.sikuli',
            timeout=30*60,
        ) as proc:
            while proc.poll() is None:
                self.save_screenshot()
                time.sleep(0.5)
