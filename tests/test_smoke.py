import unittest

from .base import BaseGUITestCase


class SmokeTest(BaseGUITestCase):
    def test_launches(self):
        self.save_screenshot()
        self.assertFalse(self.gui_proc.poll())
