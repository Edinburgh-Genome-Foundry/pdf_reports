.. raw:: html

    <p align="center">
    <img alt="DNA Chisel Logo" title="DNA Chisel" src="https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/pdf_reports/master/docs/_static/images/title.png" width="350">
    <br /><br />
    </p>

.. image:: https://travis-ci.org/Edinburgh-Genome-Foundry/pdf_reports.svg?branch=master
   :target: https://travis-ci.org/Edinburgh-Genome-Foundry/pdf_reports
   :alt: Travis CI build status

.. image:: https://coveralls.io/repos/github/Edinburgh-Genome-Foundry/pdf_reports/badge.svg?branch=master
   :target: https://coveralls.io/github/Edinburgh-Genome-Foundry/pdf_reports?branch=master


*PDF Reports* (complete documentation `here <https://edinburgh-genome-foundry.github.io/pdf_reports/>`_) is a Python library to create nice-looking PDF reports from HTML or `Pug <https://pugjs.org>`_ templates. It features modern-looking components (via the `Semantic UI <https://semantic-ui.com/>`_ framework) and provides routines to embed tables or plots in the documents.


Example of use
--------------

Your Pug template file ``template.pug`` may look like this (see a `full example <https://github.com/Edinburgh-Genome-Foundry/pdf_reports/blob/master/examples/example_template.pug>`_):

.. code:: pug

    #sidebar I am the text in the sidebar.

    h1 {{ title }}

    .ui.piled.segment
      p Oh hi there ! I am some text in a cool box.

Your Python code will be as follows:

.. code:: python

   from pdf_reports import pug_to_html, write_report
   html = pug_to_html("template.pug", title="My report")
   write_report(html, "example.pdf")

And your final result may look like this (`PDF file <https://github.com/Edinburgh-Genome-Foundry/pdf_reports/raw/master/examples/example.pdf>`_):

.. image:: https://github.com/Edinburgh-Genome-Foundry/pdf_reports/raw/master/screenshot.png

See also `this example <https://github.com/Edinburgh-Genome-Foundry/pdf_reports/blob/master/examples/with_plots_and_tables.pug>`_ embedding some python code in the template to
create figures and tables on the flight.

Special features
----------------

Markdown support
~~~~~~~~~~~~~~~~~~

As a feature of PyPugJS, markdown is supported in the Pug templates.

.. code:: pug

    div
      :markdown
        This is some markdown text. Here is a [link](http://example.com/).

        - this is a bullet point list
        - Second item
        - Etc.

PDF tools
~~~~~~~~~~

Some useful functions for generating reports are available from inside the Pug templates under ``pdf_tools``. For instance, ``pdf_tools.figure_data()`` or ``pdf_tools.dataframe_to_html()``. Have a look at the docs, or this `example <https://github.com/Edinburgh-Genome-Foundry/pdf_reports/blob/master/examples/with_plots_and_tables.pug>`_

JupyterPDF
~~~~~~~~~~~~

The ``JupyterPDF`` class eases report templates writing by embedding PDF files
in Jupyter notebooks (using the browser's interactive PDF viewer).

.. code:: python

    from pdf_reports import JupyterPDF

    # Build your PDF

    # At the end of the notebook cell:
    JupyterPDF("path_to_your.pdf")

Notes
-----

The core of the library consists of just a few lines of Python, using `pypugjs <https://github.com/akubera/pypugjs>`_ to parse Pug templates,  optionally including stylesheets from the Semantic UI CSS framework, and finally calling `weasyprint <http://weasyprint.org/>`_ for PDF generation.

Using Semantic UI implies that (1) the Lato font family should be installed on your machine, otherwise the results will look less good, and (2) the first time that ``write_pdf`` is called in a Python session, if using the default Semantic UI style, the parsing of the CSS will add a 3-second overhead to the function calls (but there will be no overhead for the next calls in that session).


Installation
-------------

You can install the library via PIP

.. code::

    sudo pip install pdf_reports

Alternatively, you can unzip the sources in a folder and type

.. code::

    sudo python setup.py install

Note: on some Debian systems you may need to first install ``libffi-dev`` (``apt install libffi-dev``). The package name may be ``libffi-devel`` on some systems.

License = MIT
--------------

This open-source software project was originally written at the `Edinburgh Genome Foundry <http://www.genomefoundry.org//>`_ by `Zulko <https://github.com/Zulko>`_
and `released on Github <https://github.com/Edinburgh-Genome-Foundry/pdf_reports>`_ under the MIT licence (¢ Edinburg Genome Foundry). Everyone is welcome to contribute !
