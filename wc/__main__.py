""" Whole-cell modeling command line interface

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2018-05-15
:Copyright: 2018, Karr Lab
:License: MIT
"""

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
import copy
import importlib
import sys
import wc


class BaseController(CementBaseController):
    """ Base controller for command line application """

    class Meta:
        label = 'base'
        description = "Whole-cell models and whole-cell modeling tools"
        arguments = [
            (['-v', '--version'], dict(action='version', version=wc.__version__)),
        ]

    @expose(hide=True)
    def default(self):
        self.app.args.print_help()


class ModelController(CementBaseController):
    """ Model controller """

    class Meta:
        label = 'model'
        description = 'Whole-cell models'
        stacked_on = 'base'
        stacked_type = 'nested'

    @expose(hide=True)
    def default(self):
        self.app.args.print_help()


class ToolController(CementBaseController):
    """ Tool controller """

    class Meta:
        label = 'tool'
        description = 'Whole-cell modeling tools'
        stacked_on = 'base'
        stacked_type = 'nested'

    @expose(hide=True)
    def default(self):
        self.app.args.print_help()


class App(CementApp):
    """ Command line application """
    class Meta:
        label = 'wc'
        base_controller = 'base'
        handlers = []

    def __init__(self, argv=None):
        self.__class__.Meta.handlers = [
            BaseController,
            ModelController,
            ToolController,
        ]

        # models
        self.add_package_handlers(argv, 'model', 'h1_hesc', 'h1_hesc')
        self.add_package_handlers(argv, 'model', 'mycoplasma_pneumoniae', 'mycoplasma_pneumoniae')

        # tools
        self.add_package_handlers(argv, 'tool', 'kinetic_datanator', 'kinetic_datanator')
        self.add_package_handlers(argv, 'tool', 'rand_wc_model_gen', 'rand_model_gen')
        self.add_package_handlers(argv, 'tool', 'wc_kb', 'kb')
        self.add_package_handlers(argv, 'tool', 'wc_lang', 'lang')
        self.add_package_handlers(argv, 'tool', 'wc_sim', 'sim')

        # super class constructor
        super(App, self).__init__(argv=argv)

    @classmethod
    def add_package_handlers(cls, argv, stacked_on, package_name, label):
        """ Add handlers for a package to add to an application

        Args:
            argv (:obj:`list` of :obj:`str`): command line arguments
            stacked_on (:obj:`str`): where the handlers for the package should be stacked
            package_name (:obj:`str`): name of the package whose handlers should be added the application
            label (:obj:`str`): root label for the handlers within the application

        Raises:
            :obj:`Exception`: if a handler is not a base or stacked on a base
        """
        if argv is None:
            argv = sys.argv[1:]

        if len(argv) < 1 or argv[0] != stacked_on:
            return
        if len(argv) >= 2 and argv[1][0] != '-' and argv[1] != label.replace('_', '-'):
            return

        module = importlib.import_module(package_name + '.__main__')

        for original_handler in module.App.Meta.handlers:
            handler = type(original_handler.__class__.__name__,
                           (original_handler, ),
                           dict(original_handler.__dict__))
            handler.Meta = type('Meta',
                                (original_handler.Meta, ),
                                dict(original_handler.Meta.__dict__))

            if handler.Meta.label == 'base':
                handler.Meta.label = label
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
                raise Exception('Invalid base handler: {}'.format(handler.Meta.label))  # pragma: no cover

            cls.Meta.handlers.append(handler)


def main():
    with App() as app:
        app.run()
