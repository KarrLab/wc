""" Whole-cell modeling command line interface

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2018-05-15
:Copyright: 2018, Karr Lab
:License: MIT
"""

from .config.core import get_config
import cement
import copy
import importlib
import sys
import wc_cli


class BaseController(cement.Controller):
    """ Base controller for command line application """

    class Meta:
        label = 'base'
        description = "Whole-cell models and whole-cell modeling tools"
        arguments = [
            (['-v', '--version'], dict(action='version', version=wc_cli.__version__)),
        ]

    @cement.ex(hide=True)
    def _default(self):
        self._parser.print_help()


class ModelController(cement.Controller):
    """ Model controller """

    class Meta:
        label = 'model'
        description = 'Whole-cell models'
        stacked_on = 'base'
        stacked_type = 'nested'

    @cement.ex(hide=True)
    def _default(self):
        self._parser.print_help()


class ToolController(cement.Controller):
    """ Tool controller """

    class Meta:
        label = 'tool'
        description = 'Whole-cell modeling tools'
        stacked_on = 'base'
        stacked_type = 'nested'

    @cement.ex(hide=True)
    def _default(self):
        self._parser.print_help()


class App(cement.App):
    """ Command line application """
    class Meta:
        label = 'wc'
        base_controller = 'base'
        handlers = []

    def __init__(self, argv=None, config=None):
        self.__class__.Meta.handlers = [
            BaseController,
            ModelController,
            ToolController,
        ]

        if not config:
            config = get_config()

        # tools
        for package_name, package_props in config['tool'].items():
            self.add_package_handlers(argv, 'tool', package_name, package_props['label'], package_props['description'])

        # models
        for package_name, package_props in config['model'].items():
            self.add_package_handlers(argv, 'model', package_name, package_props['label'], package_props['description'])

        # super class constructor
        super(App, self).__init__(argv=argv)

    @classmethod
    def add_package_handlers(cls, argv, stacked_on, package_name, label, description):
        """ Add handlers for a package to add to an application

        Args:
            argv (:obj:`list` of :obj:`str`): command line arguments
            stacked_on (:obj:`str`): where the handlers for the package should be stacked
            package_name (:obj:`str`): name of the package whose handlers should be added the application
            label (:obj:`str`): root label for the handlers within the application
            description (:obj:`str`): root descipription for the handlers within the application

        Raises:
            :obj:`SystemExit`: if a handler is not a base or stacked on a base
        """
        if argv is None:
            argv = sys.argv[1:]

        # check if package needs to be imported
        if len(argv) < 1 or argv[0] != stacked_on:
            return
        if len(argv) >= 2 and argv[1][0] != '-' and argv[1] != label.replace('_', '-'):
            return

        # add handler(s) for package
        if importlib.util.find_spec(package_name):
            # add handlers for installed package
            module = importlib.import_module(package_name + '.__main__')

            for original_handler in module.App.Meta.handlers:
                attrs = dict(original_handler.__dict__)
                handler = type(original_handler.__class__.__name__, (original_handler, ), attrs)
                handler.Meta = type('Meta', (original_handler.Meta,), dict(original_handler.Meta.__dict__))

                if handler.Meta.label == 'base':
                    handler.Meta.label = label
                    handler.Meta.description = description
                    handler.Meta.stacked_on = stacked_on
                    handler.Meta.stacked_type = 'nested'
                elif hasattr(handler.Meta, 'stacked_on'):
                    handler.Meta.aliases = [handler.Meta.label]
                    handler.Meta.aliases_only = True
                    handler.Meta.label = label + '_' + handler.Meta.label.replace('-', '_')
                    if handler.Meta.stacked_on == 'base':
                        handler.Meta.stacked_on = label
                    else:
                        handler.Meta.stacked_on = label + '_' + handler.Meta.stacked_on.replace('-', '_')
                    handler.Meta.stacked_type = 'nested'
                else:
                    raise SystemExit('Invalid base handler: {}'.format(handler.Meta.label))  # pragma: no cover

                cls.Meta.handlers.append(handler)
        else:
            # add default handler for package that is not installed
            @cement.ex(hide=True)
            def _default(self):
                raise SystemExit(('{0} must be installed to use this command. '
                                 'Run `pip install git+https://github.com/KarrLab/{0}.git` to install the package'
                                 ).format(self.Meta.package_name))  # pragma: no cover # coverage doesn't capture this
            attrs = {
                'Meta': type('Meta', (), {
                    'package_name': package_name,
                    'label': label,
                    'description': '{} (Not installed)'.format(description),
                    'stacked_on': stacked_on,
                    'stacked_type': 'nested',
                }),
                '_default': _default,
            }
            handler = type(package_name + '_Controller', (cement.Controller,), attrs)

            cls.Meta.handlers.append(handler)


def main():
    with App() as app:
        app.run()
