Tutorial
========

The following examples illustrate how to use the integrated interface to
access whole-cell models and whole-cell modeling tools.


Models
-------------------------

List the available models
~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    wc model

Get the available operations for a model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    wc model h1-hesc

Run a model operation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    wc model h1-hesc sim


Tools
-------------------------

List the available tools
~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    wc tool

Get the operations for a tool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    wc tool lang

Run an operation of a tool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    wc tool lang validate /path/to/model.xlsx


Help
-------------------------

Get help
~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    wc --help