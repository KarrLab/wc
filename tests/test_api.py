""" Tests API

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2018-05-16
:Copyright: 2018, Karr Lab
:License: MIT
"""

import wc_cli
import types
import unittest


class ApiTestCase(unittest.TestCase):
    def test(self):
        self.assertIsInstance(wc_cli, types.ModuleType)
        self.assertIsInstance(wc_cli.config, types.ModuleType)
        self.assertIsInstance(wc_cli.config.get_config, types.FunctionType)
