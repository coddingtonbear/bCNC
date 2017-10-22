import contextlib
import os
import unittest
import subprocess
import time

import pyscreenshot


class SikuliError(Exception):
    pass


class SikuliTimeout(SikuliError):
    pass


class BaseGUITestCase(unittest.TestCase):
    SCREENSHOT_DIR = os.path.join(
        os.path.dirname(__file__),
        '../screenshots/'
    )

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

        self.screenshot_counter = 0

        # We need to give the GUI enough time to start up; this is
        # probably enough, but ideally we'd just check for the presence
        # of the window so we don't wait unnecessarily.
        time.sleep(5)

    def _run_sikuli(self, name):
        proc = subprocess.Popen([
            os.path.join(
                self.build_dir,
                'runsikulix'
            ),
            '-r',
            os.path.join(
                self.build_dir,
                'tests/scripts/',
                name,
            )
        ])
        return proc

    @contextlib.contextmanager
    def async_sikuli_script(self, name, timeout=30):
        started = time.time()
        proc = self._run_sikuli(name)
        yield proc
        while proc.poll() is None:
            if time.time() > started + timeout:
                proc.kill()
                raise SikuliTimeout()
            time.sleep(0.1)
        if proc.returncode != 0:
            raise SikuliError(proc.returncode)

    def run_sikuli_script(self, *args, **kwargs):
        with self.async_sikuli_script(*args, **kwargs) as proc:
            return proc.wait()

    def save_screenshot(self, name=None):
        if name is None:
            name = '{test_name}.{counter}.png'.format(
                test_name=self.id(),
                counter=self.screenshot_counter
            )
        print "Saving screenshot as " + name

        if not os.path.isdir(self.SCREENSHOT_DIR):
            os.mkdir(self.SCREENSHOT_DIR)

        im = pyscreenshot.grab()
        im.save(
            os.path.join(
                self.SCREENSHOT_DIR,
                name,
            )
        )
        self.screenshot_counter += 1

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
