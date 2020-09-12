PDF Reports
===========

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

Infos
-----

**PIP installation:**

.. code:: bash

  pip install pdf_reports

**Web documentation:**

`<https://edinburgh-genome-foundry.github.io/pdf_reports/>`_

**Github Page:**

`<https://github.com/Edinburgh-Genome-Foundry/pdf_reports>`_

**Live demo:**

`<http://cuba.genomefoundry.org/sculpt_a_sequence>`_

**License:** MIT, Copyright Edinburgh Genome Foundry
