.. raw:: html

    <p align="center">
    <img alt="PDF Reports Logo" title="PDF Reports" src="https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/pdf_reports/master/docs/_static/images/title.png" width="350">
    <br /><br />
    </p>


PDF_Reports
===========

.. image:: https://travis-ci.com/Edinburgh-Genome-Foundry/pdf_reports.svg?branch=master
   :target: https://travis-ci.com/Edinburgh-Genome-Foundry/pdf_reports
   :alt: Travis CI build status

.. image:: https://coveralls.io/repos/github/Edinburgh-Genome-Foundry/pdf_reports/badge.svg?branch=master
   :target: https://coveralls.io/github/Edinburgh-Genome-Foundry/pdf_reports?branch=master



*PDF Reports* (complete documentation `here <https://edinburgh-genome-foundry.github.io/pdf_reports/>`_) is a Python library to create nice-looking PDF reports from HTML or `Pug <https://pugjs.org>`_ templates. It features modern-looking components (via the `Semantic UI <https://semantic-ui.com/>`_ framework) and provides routines to embed tables or plots in the documents.

Note that only Python 3.x is officially supported, although with the right version of weasyprint the library can also run on 2.x.


Example of use
--------------

Your Pug template file ``template.pug`` may look like this (see a `full example <https://github.com/Edinburgh-Genome-Foundry/pdf_reports/blob/master/examples/basic_example/example_template.pug>`_):

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

And your final result may look like this (`PDF file <https://github.com/Edinburgh-Genome-Foundry/pdf_reports/raw/master/examples/basic_example/example.pdf>`_):

.. image:: https://github.com/Edinburgh-Genome-Foundry/pdf_reports/raw/master/screenshot.png

See also `this example <https://github.com/Edinburgh-Genome-Foundry/pdf_reports/blob/master/examples/example_with_plot_and_tables/with_plots_and_tables.pug>`_ embedding some python code in the template to
create figures and tables on the flight.


Other features
--------------


Preloading CSS and  SCSS
~~~~~~~~~~~~~~~~~~~~~~~~

PDF Reports provides a ``preload_stylesheet`` method which can be used to load
and parse a CSS file. It also works with SCSS files (which will automatically
be compiled to CSS) but this requires ``libsass`` installed (for instance via
``pip install libsass``). Here is an example:

.. code:: python

    from pdf_reports import pug_to_html, write_report, preload_stylesheet

    css = preload_stylesheet('style.scss')
    html = pug_to_html("template.pug", title="My report", my_name='Zulko')
    write_report(html, "example.pdf", extra_stylesheets=[css])


Using a ReportWriter
~~~~~~~~~~~~~~~~~~~~

The ReportWriter class allows to define default templates, styles, and variable
names. It can be used to avoid repeating yourself across your application:

.. code:: python

    from pdf_reports import ReportWriter

    # DEFINE A WRITER WITH DEFAULT TEMPLATE AND VALUES
    report_writer = ReportWriter(
        default_stylesheets=["style.css"],
        default_template="template.pug",
        title="My default title",
        version="0.1.2"
    )

    # THEN LATER IN YOUR CODE:
    html = report_writer.pug_to_html(my_name="Zulko", my_organization="EGF")
    report_writer.write_report(html, "example_reportwriter.pdf")


Markdown support
~~~~~~~~~~~~~~~~

As a feature of PyPugJS, markdown is supported in the Pug templates.

.. code:: pug

    div
      :markdown
        This is some markdown text. Here is a [link](http://example.com/).

        - this is a bullet point list
        - Second item
        - Etc.


PDF tools
~~~~~~~~~

Some useful functions for generating reports are available from inside the
Pug templates under ``pdf_tools``. For instance, ``pdf_tools.figure_data()``
to embed matplotlib images, or ``pdf_tools.dataframe_to_html()``
to turn Pandas dataframes into HTML, and style them nicely with Semantic UI.
Have a look at the docs, or this
`example <https://github.com/Edinburgh-Genome-Foundry/pdf_reports/blob/master/examples/example_with_plot_and_tables/with_plots_and_tables.pug>`_.


JupyterPDF
~~~~~~~~~~

The ``JupyterPDF`` class eases report templates writing by embedding PDF files
in Jupyter notebooks (using the browser's interactive PDF viewer).

.. code:: python

    from pdf_reports import JupyterPDF

    # Build your PDF

    # At the end of the notebook cell:
    JupyterPDF("path_to_your.pdf")


Notes
-----

The core of the library consists of just a few lines of Python, using `pypugjs <https://github.com/akubera/pypugjs>`_ to parse Pug templates, optionally including stylesheets from the Semantic UI CSS framework, and finally calling `weasyprint <http://weasyprint.org/>`_ for PDF generation. Please refer to the Weasyprint documentation for the customization of templates. For instance, to customize the page margins and numbering the Weasyprint way, add this to your SCSS code:

.. code:: scss

    @page {
        margin: 1cm 0 2cm 0cm;
        @bottom-center {
            content: "Page " counter(page) " / " counter(pages);
            font-family: 'Lato';
        }
    }


Using Semantic UI implies that (1) the Lato font family should be installed on your machine, otherwise the results will look less good, and (2) the first time that ``write_pdf`` is called in a Python session, if using the default Semantic UI style, the parsing of the CSS will add a 3-second overhead to the function calls (but there will be no overhead for the next calls in that session).


Installation
------------

You can install the library via PIP:

.. code::

    pip install pdf_reports

Alternatively, you can unzip the sources in a folder and type:

.. code::

    python setup.py install

**Note:** the package depends on the WeasyPrint Python package. If there are any issues, see installation instructions
in the `WeasyPrint documentation <https://doc.courtbouillon.org/weasyprint/stable/first_steps.html>`_.
The version is `fixed to <=52 <https://github.com/Edinburgh-Genome-Foundry/pdf_reports/blob/master/setup.py>`_
as not all GNU/Linux distributions have the latest Pango that is required by the latest WeasyPrint.

**Note: on some Debian systems** you may need to first install ``libffi-dev`` (``apt install libffi-dev``). The package name may be ``libffi-devel`` on some systems.

**Note: on macOS,** you may need to first install pango with: ``brew install pango``


License = MIT
-------------

This open-source software project was originally written at the `Edinburgh Genome Foundry <http://www.genomefoundry.org//>`_ by `Zulko <https://github.com/Zulko>`_
and `released on Github <https://github.com/Edinburgh-Genome-Foundry/pdf_reports>`_ under the MIT licence (Copyright 2018 Edinburgh Genome Foundry). Everyone is welcome to contribute !
