import os
from pdf_reports import pug_to_html, write_report, preload_stylesheet, ReportWriter
import pandas
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader


def test_pug_to_html():
    html = pug_to_html(string="p {{ var }}", var="Bla")
    assert html == "<p>Bla</p>"


def test_write_pdf():
    data = write_report("<h1>Test</h1>")
    assert len(data) > 100


def test_basics(tmpdir):
    template_path = os.path.join("tests", "data", "example_template.pug")
    assert os.path.exists(template_path)
    pdf_path = os.path.join(str(tmpdir), "test.pdf")
    html = pug_to_html(template_path, title="Summary of your order")
    write_report(html, pdf_path)
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        assert len(reader.pages) == 2

    pdf_data = write_report(html)
    assert len(pdf_data) > 10000


def test_with_plots_and_tables(tmpdir):
    template_path = os.path.join("tests", "data", "with_plots_and_tables.pug")
    assert os.path.exists(template_path)

    dataframe = pandas.DataFrame.from_records(
        {
            "Name": ["Anna", "Bob", "Claire", "Denis"],
            "Age": [12, 22, 33, 44],
            "Height (cm)": [140, 175, 173, 185],
        },
        columns=["Name", "Age", "Height (cm)"],
    )

    pdf_path = os.path.join(str(tmpdir), "test.pdf")
    html = pug_to_html(template_path, dataframe=dataframe)
    write_report(html, pdf_path)
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        assert len(reader.pages) == 2

    pdf_data = write_report(html)
    assert len(pdf_data) > 10000


def test_preload_stylesheet(tmpdir):
    css = preload_stylesheet(os.path.join("tests", "data", "style.scss"))
    html = pug_to_html(string="p {{ var }}", var="Bla")
    pdf_path = os.path.join(str(tmpdir), "test.pdf")
    write_report(html, pdf_path, extra_stylesheets=[css])


def test_ReportWriter(tmpdir):
    report_writer = ReportWriter(
        default_template=os.path.join("tests", "data", "template_rw.pug"),
        title="My default title",
        version="0.1.2",
    )
    html = report_writer.pug_to_html(my_name="Zulko", my_organization="EGF")
    report_writer.write_report(html, os.path.join(str(tmpdir), "test_rw.pdf"))
