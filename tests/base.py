import os
import unittest
import subprocess
import time


class BaseGUITestCase(unittest.TestCase):
    def setUp(self):
        self.build_dir = os.environ.get(
            'TRAVIS_BUILD_DIR',
            os.path.join(
                os.path.dirname(__file__),
                '../',
            )
        )

        self.gui_proc = subprocess.Popen([
            self.get_python_path(),
            os.path.join(
                self.build_dir,
                'bCNC.py',
            )
        ])

        # We need to give the GUI enough time to start up; this is
        # probably enough, but ideally we'd just check for the presence
        # of the window so we don't wait unnecessarily.
        time.sleep(5)

    def get_python_path(self):
        virtual_env = os.environ.get('VIRTUAL_ENV')

        if virtual_env:
            return os.path.join(
                virtual_env,
                'bin/python'
            )

        return '/usr/local/bin/python'

    def tearDown(self):
        max_termination_wait_seconds = 5
        terminated = time.time()
        self.gui_proc.terminate()

        while(time.time() < terminated + max_termination_wait_seconds):
            if self.gui_proc.poll():
                return

        # If we've made it this far, the process is still running
        self.gui_proc.kill()
