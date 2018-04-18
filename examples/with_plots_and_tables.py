"""PDF report generation from a Pug template embedding code to generate
plots and tables.

A HTML page is generated from a template and rendered as a local PDF file.
"""

import pandas
import matplotlib.pyplot as plt
from pdf_reports import pug_to_html, write_report

dataframe = pandas.DataFrame.from_records({
    "Name": ["Anna", "Bob", "Claire", "Denis"],
    "Age": [12,22,33,44],
    "Height (cm)": [140, 175, 173, 185]
}, columns=["Name", "Age", "Height (cm)"])

html = pug_to_html("with_plots_and_tables.pug", dataframe=dataframe)
write_report(html, "with_plots_and_tables.pdf")
