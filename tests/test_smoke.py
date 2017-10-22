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

        self.run_sikuli_script('run_sample_gcode.sikuli')

        while self.get_bcnc_state()['state'] != 'Idle':
            self.save_screenshot()
            print self.get_bcnc_state()
            time.sleep(0.5)

        self.assertTrue(
            'Complete' in self.get_bcnc_state()['msg']
        )
