import contextlib
import os
import unittest
import subprocess
import time

import imageio
import pyscreenshot
import requests


class SikuliError(Exception):
    pass


class SikuliTimeout(SikuliError):
    pass


class BaseGUITestCase(unittest.TestCase):
    SCREENSHOT_DIR = os.path.join(
        os.path.dirname(__file__),
        '../screenshots/'
    )
    DEFAULT_SCREENSHOT_FRAME_DURATION = 0.5

    def setUp(self):
        super(BaseGUITestCase, self).setUp()
        self.screenshot_counter = 0
        self.screenshots = []

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
        self.run_sikuli_script('focus_bCNC.sikuli')

        self.save_screenshot()

    def tearDown(self):
        self.save_screenshot()

        # Create an animated gif of the captured screenshots for this test.
        images = []
        durations = []
        prev_screenshot_time = None
        for screenshot in self.screenshots:
            images.append(imageio.imread(screenshot['filename']))
            os.unlink(screenshot['filename'])
            if prev_screenshot_time:
                durations.append(
                    screenshot['time'] - prev_screenshot_time
                )
            else:
                durations.append(self.DEFAULT_SCREENSHOT_FRAME_DURATION)
            prev_screenshot_time = screenshot['time']

        imageio.mimsave(
            os.path.join(
                self.SCREENSHOT_DIR,
                '{test_name}.gif'.format(
                    test_name=self.id()
                )
            ),
            images,
            duration=durations,
        )

        max_termination_wait_seconds = 5
        terminated = time.time()
        self.gui_proc.terminate()

        while(time.time() < terminated + max_termination_wait_seconds):
            if self.gui_proc.poll():
                return

        # If we've made it this far, the process is still running
        self.gui_proc.kill()

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
            if timeout and time.time() > started + timeout:
                proc.kill()
                raise SikuliTimeout()
            time.sleep(0.1)
        if proc.returncode != 0:
            raise SikuliError(proc.returncode)

    def run_sikuli_script(self, *args, **kwargs):
        with self.async_sikuli_script(*args, **kwargs) as proc:
            return proc.wait()

    def get_bcnc_state(self):
        return requests.get('http://127.0.0.1:5001/state').json()

    def get_static_path(self, filename):
        return os.path.join(
            self.build_dir,
            'tests/static/',
            filename,
        )

    def save_screenshot(self, name=None):
        if name is None:
            name = '{test_name}.{counter}.png'.format(
                test_name=self.id(),
                counter=self.screenshot_counter
            )

        if not os.path.isdir(self.SCREENSHOT_DIR):
            os.mkdir(self.SCREENSHOT_DIR)

        absolute_path = os.path.join(
            self.SCREENSHOT_DIR,
            name,
        )

        im = pyscreenshot.grab()
        im.save(absolute_path)
        self.screenshot_counter += 1

        self.screenshots.append({
            'time': time.time(),
            'filename': name,
        })

    def get_python_path(self):
        virtual_env = os.environ.get('VIRTUAL_ENV')

        if virtual_env:
            return os.path.join(
                virtual_env,
                'bin/python'
            )

        return '/usr/local/bin/python'
