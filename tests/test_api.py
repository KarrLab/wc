""" Tests API

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2018-05-16
:Copyright: 2018, Karr Lab
:License: MIT
"""

import wc
import types
import unittest


class ApiTestCase(unittest.TestCase):
    def test(self):
        self.assertIsInstance(wc, types.ModuleType)
        self.assertIsInstance(wc.config, types.ModuleType)
        self.assertIsInstance(wc.config.get_config, types.FunctionType)
