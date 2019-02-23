"""Basic PDF report generation from a Pug template with pdf_reports.

A HTML page is generated from a template and rendered as a local PDF file.
"""

from pdf_reports import pug_to_html, write_report

html = pug_to_html("example_template.pug", title="My report")
write_report(html, "example.pdf")
