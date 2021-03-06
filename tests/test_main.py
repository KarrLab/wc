""" Tests of wc_cli command line interface (wc_cli.__main__)

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2018-05-15
:Copyright: 2018, Karr Lab
:License: MIT
"""

from wc_cli import __main__
import capturer
import mock
import os
import tempfile
import unittest
import wc_cli


class TestCore(unittest.TestCase):
    def setUp(self):
        fid, self.filename = tempfile.mkstemp(suffix='.xlsx')
        os.close(fid)

    def tearDown(self):
        os.remove(self.filename)

    def test_cli(self):
        with mock.patch('sys.argv', ['wc-cli', '--help']):
            with self.assertRaises(SystemExit) as context:
                __main__.main()
                self.assertRegex(context.Exception, 'usage: wc-cli')

    def test_help(self):
        with self.assertRaises(SystemExit):
            with __main__.App(argv=['--help']) as app:
                app.run()
            self.assertRegex(context.Exception, 'usage: wc-cli')

        with capturer.CaptureOutput(merged=False, relay=False) as captured:
            with __main__.App(argv=[]) as app:
                app.run()
            self.assertRegex(captured.stdout.get_text(), 'usage: wc-cli')
            self.assertEqual(captured.stderr.get_text(), '')

    def test_version(self):
        with __main__.App(argv=['-v']) as app:
            with capturer.CaptureOutput(merged=False, relay=False) as captured:
                with self.assertRaises(SystemExit):
                    app.run()
                self.assertEqual(captured.stdout.get_text(), wc_cli.__version__)
                self.assertEqual(captured.stderr.get_text(), '')

        with __main__.App(argv=['--version']) as app:
            with capturer.CaptureOutput(merged=False, relay=False) as captured:
                with self.assertRaises(SystemExit):
                    app.run()
                self.assertEqual(captured.stdout.get_text(), wc_cli.__version__)
                self.assertEqual(captured.stderr.get_text(), '')

    def test_model_help(self):
        config = {
            'tool': {},
            'model': {
                'mycoplasma_pneumoniae': {
                    'label': 'mycoplasma_pneumoniae',
                    'description': 'Whole-cell model of Mycoplasma pneumoniae',
                }
            },
        }

        with capturer.CaptureOutput(merged=False, relay=False) as captured:
            with __main__.App(argv=['model'], config=config) as app:
                # run app
                app.run()

                # test that the CLI produced the correct output
                self.assertRegex(captured.stdout.get_text(), 'mycoplasma-pneumoniae')
                self.assertEqual(captured.stderr.get_text(), '')

    def test_model_not_installed(self):
        config = {
            'tool': {},
            'model': {
                'not_installed_model': {
                    'label': 'not_installed_model',
                    'description': 'A model that is not installed',
                },
            },
        }

        with self.assertRaises(SystemExit) as context:
            with __main__.App(argv=['model', 'not-installed-model', '--help'], config=config) as app:
                # run app
                app.run()
            self.assertRegex(context.Exception, 'must be installed to use this command')

    def test_tool_help(self):
        config = {
            'tool': {
                'wc_kb': {
                    'label': 'kb',
                    'description': 'Framework for knowledge bases for whole-cell models',
                },
                'wc_lang': {
                    'label': 'lang',
                    'description': 'Framework for representing whole-cell models',
                },
            },
            'model': {},
        }

        with capturer.CaptureOutput(merged=False, relay=False) as captured:
            with __main__.App(argv=['tool'], config=config) as app:
                # run app
                app.run()

                # test that the CLI produced the correct output
                self.assertRegex(captured.stdout.get_text(), 'kb')
                self.assertRegex(captured.stdout.get_text(), 'lang')
                self.assertEqual(captured.stderr.get_text(), '')

    def test_tool_wc_lang(self):
        with capturer.CaptureOutput(merged=False, relay=False) as captured:
            with __main__.App(argv=['tool', 'lang', '--version']) as app:
                # run app
                app.run()
            self.assertRegex(captured.stdout.get_text(), r'^\d+\.\d+\.\d+[a-zA-Z0-9]*$')
            self.assertEqual(captured.stderr.get_text(), '')

    def test_tool_wc_lang(self):
        os.remove(self.filename)

        with __main__.App(argv=['tool', 'lang', 'create-template', self.filename, '--ignore-repo-metadata']) as app:
            # run app
            app.run()

        self.assertTrue(os.path.isfile(self.filename))
