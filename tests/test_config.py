""" Tests of config module

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2018-05-16
:Copyright: 2018, Karr Lab
:License: MIT
"""

from wc import config
import unittest


class ConfigTestCase(unittest.TestCase):
    def test_get_config(self):
        vals = config.get_config()

        # tools
        self.assertIsInstance(vals['tool'], dict)
        self.assertGreater(len(vals['tool']), 0)
        for tool in vals['tool'].values():
            self.assertIn('label', tool)
        self.assertEqual(vals['tool']['wc_lang']['label'], 'lang')
        self.assertEqual(vals['tool']['wc_lang']['description'], 'Framework for representing whole-cell models')

        # models
        self.assertIsInstance(vals['model'], dict)
        self.assertGreater(len(vals['model']), 0)
        for model in vals['model'].values():
            self.assertIn('label', model)
        self.assertEqual(vals['model']['h1_hesc']['label'], 'h1_hesc')
