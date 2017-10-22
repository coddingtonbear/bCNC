import shutil
import time

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
        self.send_command('run')
        print self.get_bcnc_state()
        self.save_screenshot()

        time.sleep(5)
        print self.get_bcnc_state()
        self.send_command('stop')
        print self.get_bcnc_state()
        self.save_screenshot()
        print self.get_bcnc_state()
