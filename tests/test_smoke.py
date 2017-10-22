import unittest

from .base import BaseGUITestCase


class SmokeTest(BaseGUITestCase):
    def test_launches(self):
        self.assertFalse(self.gui_proc.poll())

    def test_can_open_terminal(self):
        self.run_sikuli_script('open_terminal.sikuli')
